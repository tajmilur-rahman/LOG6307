package com.querel.log6307.linking.model;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

/**
 * Created by lquerel on 9/22/14.
 */
public class DatabaseUtils {

    final static Logger logging = LoggerFactory.getLogger("Utils");

    public static List<String> getListOfCommits(Database database){

        try {
            ResultSet resultSet = database.selectDistinctCommits();

            resultSet.first();
            Stack commits = new Stack();
            do{
                commits.push(resultSet.getString("commit"));
            } while (resultSet.next());

            return commits;

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;

    }

    public static List<Commit> getListOfCommitMetricId(Database database){

        try {
            ResultSet resultSet = database.selectListOfCommitMetricIds();

            resultSet.first();
            List<Commit> commits = new LinkedList<Commit>();
            do{
                commits.add(new Commit(resultSet.getString("commit"), resultSet.getString("subject"), resultSet.getString("log")));
            } while (resultSet.next());

            return commits;
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return null;
    }

    public static HashMap<Integer, String> getMapOfIssues(Database database){

        try {
            ResultSet resultSet = database.selectAllIssues();

            resultSet.first();
            HashMap<Integer, String> issues = new HashMap<Integer, String>();
            do{
                issues.put(resultSet.getInt("id"), resultSet.getString("type"));
            } while (resultSet.next());

            return issues;

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;

    }

    public static void populateCommitMetricData(Database database, String commitId) throws SQLException {

        List<Revision> revisions = getListOfRevisions(database, commitId);

        HashSet<String> modifiedSubsystems = new HashSet<String>();
        HashSet<String> modifiedDirectories = new HashSet<String>();

        CommitMetric commitMetric = new CommitMetric(commitId);
        commitMetric.setNumberOfModifiedFiles(revisions.size());


        for (int i = 0; i < revisions.size(); i++) {
            Revision revision = revisions.get(i);

            String path = revision.getCanonical();

            if (path.contains("/")) {
                modifiedSubsystems.add(path.substring(0, path.indexOf('/')));
                modifiedDirectories.add(path.substring(0, path.lastIndexOf('/')));
            } else {
                modifiedSubsystems.add("/");
                modifiedDirectories.add("/");
            }
        }

        commitMetric.setNumberOfModifiedSubsystems(modifiedSubsystems.size());
        commitMetric.setNumberOfModifiedDirectories(modifiedDirectories.size());

        database.updateCommitMetric(commitMetric);

    }

    private static List<Revision> getListOfRevisions(Database database, String commitId) throws SQLException {

        ResultSet resultSet = database.getCommitRevisions(commitId);

        List<Revision> revisions = new LinkedList<Revision>();

        if (resultSet.first()) {



            do {
                int linesAdded = resultSet.getInt("add");
                int linesRemove = resultSet.getInt("remove");
                String path = resultSet.getString("path");
                String old_path = resultSet.getString("old_path");
                String new_path = resultSet.getString("new_path");
                String canonical = resultSet.getString("canonical");

                revisions.add(new Revision(commitId, linesAdded, linesRemove, path, old_path, new_path, canonical));

            } while (resultSet.next());

        }
        return revisions;
    }

}
