package com.querel.log6307.linking.model;

import lombok.Data;

/**
 * Created by lquerel on 9/23/14.
 */

@Data
public class CommitMetric {

    private String commitId;

    private Integer numberOfModifiedSubsystems = null;
    private Integer numberOfModifiedDirectories = null;
    private Integer numberOfModifiedFiles = null;
    private float entropy;

    private float linesOfCodeAdded;
    private float linesOfCodeDeleted;
    private float linesOfCodeInFiles;

    public CommitMetric(String commitId){
        this.commitId = commitId;
    }

    public String generateQueryValues(){
        
        boolean isThisFirstValue = true;
        
        StringBuilder values = new StringBuilder();

        isThisFirstValue = buildQuery(isThisFirstValue, values, this.getNumberOfModifiedSubsystems(), "ns");
        isThisFirstValue = buildQuery(isThisFirstValue, values, this.numberOfModifiedDirectories, "nd");
        isThisFirstValue = buildQuery(isThisFirstValue, values, this.getNumberOfModifiedFiles(), "nf");

        return values.toString();
    }

    private boolean buildQuery(Boolean first, StringBuilder values, Integer value, String columnName){
        if (value == null){
            return first;
        } else {
            if (!first){
                values.append(", ");
            }
            values.append(columnName).append(" = ").append(value);
            return false;
        }

    }
}



