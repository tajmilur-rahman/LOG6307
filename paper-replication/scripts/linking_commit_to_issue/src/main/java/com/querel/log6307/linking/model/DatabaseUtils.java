package com.querel.log6307.linking.model;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Stack;

/**
 * Created by lquerel on 9/22/14.
 */
public class DatabaseUtils {

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
    
}
