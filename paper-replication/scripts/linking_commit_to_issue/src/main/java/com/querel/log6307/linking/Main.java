package com.querel.log6307.linking;

import com.querel.log6307.linking.model.Database;
import com.querel.log6307.linking.model.DatabaseUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.BatchUpdateException;
import java.sql.SQLException;
import java.util.List;

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
        List commits = DatabaseUtils.getListOfCommits(database);
        logging.info(commits.size() + " unique commits were identified");

        logging.info("Populating linking table with commits present");

        try {
            database.createLinkingTable(commits);
        } catch (BatchUpdateException e){
            logging.error(e.getNextException().getMessage());
        } catch (SQLException e) {
            e.printStackTrace();
        }

        //logging.info("Extracting commits which ")

    }
}
