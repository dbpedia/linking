package com.ontosim.config;

import java.util.HashSet;
import java.util.Set;

import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;

import com.ontosim.service.OntoSimService;
import com.ontosim.util.CorsFilter;

@ApplicationPath("/") 
public class ApplicationConfig extends Application{

    @Override
    public Set<Class<?>> getClasses() {
    	System.out.println("Application Config");
        final Set<Class<?>> returnValue = new HashSet<Class<?>>();
        returnValue.add(OntoSimService.class);
        returnValue.add(CorsFilter.class);
        return returnValue;
    }
}
