package com.querel.log6307.linking.model;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Created by lquerel on 9/23/14.
 */
@Data
@AllArgsConstructor
public class Commit {

    private String commitId;
    private String summary;
    private String log;

}
