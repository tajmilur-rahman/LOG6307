package com.querel.log6307.linking;

import com.querel.log6307.linking.model.Commit;
import com.querel.log6307.linking.model.Database;
import com.querel.log6307.linking.model.DatabaseUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.BatchUpdateException;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {

    final static Logger logging = LoggerFactory.getLogger("MAIN");

    public static void main(String[] args) {

        logging.info("Git to Trac Linker Started");
        // So we would need to get the database information from a config file or through the command parameters, but for
        // now let's keep it like this

        String username = "lquerel";
        String password = "password";
        String databaseName = "assignment";
        String hostname = "localhost";

        Database database = null;

        try {
            database = new Database(username, password, hostname, databaseName);
        } catch (SQLException e) {
            logging.error("Error with database: " + e.getMessage());
            System.exit(1);
        }

        logging.info("Successfully connected to database. Starting linking process");

        // Attempt to get list of the commits
        List<String> commits = DatabaseUtils.getListOfCommits(database);
        logging.info(commits.size() + " unique commits were identified");

        logging.info("Initial populating commit metric table with commits present started");

        try {
            database.createCommitMetricTable(commits);
        } catch (BatchUpdateException e){
            logging.error(e.getNextException().getMessage());
        } catch (SQLException e) {
            e.printStackTrace();
        }

        logging.info("Initial populating commit metric table with commits present completed");

        logging.info("Calculating values and linking commit to issue if present");

        HashMap<Integer, String> issues = DatabaseUtils.getMapOfIssues(database);
        List<Commit> metricCommits = DatabaseUtils.getListOfCommitMetricId(database);

        int numberOfIssues = issues.size();
        int numberOfCommits = metricCommits.size();
        logging.info(String.valueOf(numberOfIssues));

        for (int i = 0; i < numberOfCommits; i++){

            Commit commit = metricCommits.get(i);

            String commitId = commit.getCommitId();
            logging.info("Processing commit "+(i+1)+" of "+numberOfCommits+" - "+commitId);
            try {
                DatabaseUtils.populateCommitMetricData(database, commitId);
            } catch (SQLException e) {
                e.printStackTrace();
                break;
            }

            String commit_summary = commit.getSummary();

            Pattern issueNumberPattern = Pattern.compile("#\\d+");
            Matcher matcher = issueNumberPattern.matcher(commit_summary);
            if (matcher.find()){
                int id = Integer.parseInt(commit_summary.substring(matcher.start() + 1, matcher.end()));
                logging.info("match found : #"+id);

                try {
                    database.createCommitIssueLink(commitId, id);
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }

            //logging.info("Linked commit "+(i+1)+" of "+numberOfCommits+" to issue #"+1);

        }

    }
}
