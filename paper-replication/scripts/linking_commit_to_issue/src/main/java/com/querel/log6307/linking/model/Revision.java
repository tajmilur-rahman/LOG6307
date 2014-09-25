package com.querel.log6307.linking.model;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Created by lquerel on 9/22/14.
 */

@AllArgsConstructor
@Data
public class Revision {

    private String commit;
    private int linesAdded;
    private int linesRemoved;
    private String path;
    private String old_path;
    private String new_path;
    private String canonical;

}
