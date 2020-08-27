package com.ontosim.adapter;

import java.util.concurrent.Future;

/**
 * 
 *
 * @author Michael Roder
 * Created on 12 Feb 2018
 *
 */
public class FileReceiverCallableState {

    public final Future<String[]> result;
    
    public final FileReceiverCallable callable;

    public FileReceiverCallableState(Future<String[]> result, FileReceiverCallable callable) {
        super();
        this.result = result;
        this.callable = callable;
    }
}
