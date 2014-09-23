package com.querel.log6307.linking.model;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.util.List;

/**
 * Created by lquerel on 9/22/14.
 * Louis-Philippe Querel
 * lquerel@gmail.com
 */
public class Database {

    final static Logger logger = LoggerFactory.getLogger("DATABASE");


    private String username;
    private String password;
    private String hostname;
    private String databaseName;

    private Connection connection;

    private int batchSize = 500;


    public Database(String username, String password, String hostname, String databaseName) throws SQLException {

        this.username = username;
        this.password = password;
        this.hostname = hostname;
        this.databaseName = databaseName;

        try {
            ClassLoader.getSystemClassLoader().loadClass("org.postgresql.Driver");
        } catch (ClassNotFoundException e) {
            System.out.println("class not found");
            e.printStackTrace();
        }

        connection = DriverManager.getConnection("jdbc:postgresql://"+hostname+"/"+databaseName, username, password);
    }

    public ResultSet selectDistinctCommits() throws SQLException {

        // So right now we are getting all of the commit ids, but we should probably do this in batches to make it more efficient
        CallableStatement statement = connection.prepareCall("SELECT DISTINCT(COMMIT) FROM GIT_COMMIT;", ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
        return statement.executeQuery();
    }

    public ResultSet selectAllIssues() throws SQLException {

        CallableStatement statement = this.connection.prepareCall("SELECT ID, TYPE FROM LOG6307_ISSUES;",ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
        return statement.executeQuery();
    }

    public ResultSet selectListOfCommitMetricIds() throws SQLException {

        CallableStatement statement = this.connection.prepareCall("SELECT COMMIT FROM LOG6307_COMMIT;",ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
        return statement.executeQuery();
    }

    public void createCommitMetricTable(List commits) throws SQLException {

        int listSize = commits.size();
        int index = 0;

        Statement statement = this.connection.createStatement();

        for (int i = index; i < 20; i++) {
        //for (int i = index; i < listSize; i++) {
            String query = "INSERT INTO LOG6307_COMMIT(commit) values ('"+commits.get(i)+"')";
            statement.addBatch(query);

        }
        statement.executeBatch();
        statement.close();

    }

    public void updateCommitMetric(CommitMetric commitMetric) throws SQLException {

        CallableStatement statement = this.connection.prepareCall("UPDATE LOG6307_COMMIT SET "+
                commitMetric.generateQueryValues()+" WHERE COMMIT = '"+commitMetric.getCommitId()+"'",ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
        statement.execute();


    }

    public ResultSet getCommitRevisions(String commitId) throws SQLException {
        PreparedStatement statement = this.connection.prepareStatement("SELECT * FROM GIT_REVISION WHERE COMMIT = '"+commitId+"';",ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
        return statement.executeQuery();
    }

}
