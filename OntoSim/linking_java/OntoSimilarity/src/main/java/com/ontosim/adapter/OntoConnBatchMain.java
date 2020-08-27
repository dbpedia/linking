package com.ontosim.adapter;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OntoConnBatchMain {
	
	private static final Logger logger = LoggerFactory.getLogger(OntoConnBatchMain.class);

	
	public static void main(String args[]) {

		logger.info("#################### OntoSim Batch START ####################");
		
		try{
			
			String ontoFlPath = System.getProperty("user.dir") + File.separator + "ontofiles/local";
			String srcFlPath = ontoFlPath + File.separator + "source.owl";
			String trgtFlPath = ontoFlPath + File.separator + "target.owl";

			String currTimeStamp = new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss").format(new Date());
			String resultsPath = ontoFlPath + File.separator + "result_"+currTimeStamp+".rdf";
			
			// Calling OntoConnController
			OntoConnController ontoConnController = new OntoConnController();
			ontoConnController.ontoConnController(srcFlPath, trgtFlPath, resultsPath, "Anatomy");
			
		}catch(Exception e){
			logger.error("Exception occur:- ", e);
		}

		logger.info("#################### OntoSim Batch STOP ####################");
	}

}
