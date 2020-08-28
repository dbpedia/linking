package com.ontosim.adapter;

import java.io.File;
import java.text.SimpleDateFormat;
import java.time.Duration;
import java.time.Instant;
import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OntoConnBatchMain {
	
	private static final Logger logger = LoggerFactory.getLogger(OntoConnBatchMain.class);

	
	public static void main(String args[]) {

		logger.info("#################### OntoSim Batch START ####################");
		Instant start = Instant.now();
		
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
		}finally{
			Instant end = Instant.now();
			Duration timeElapsed = Duration.between(start, end);
			long ms = timeElapsed.toMillis();
			System.out.println("Time taken: "+ ms +" milliseconds");
			
			
			long diffSeconds = (ms / 1000) % 60;
			long diffMinutes = (ms / (60 * 1000)) % 60;
			long diffHours = (ms / (60 * 60 * 1000)) % 24;

			System.out.println("Time taken: "+ diffHours +" hours, "+ diffMinutes +" minutes, "+ diffSeconds +" seconds.");

		}

		logger.info("#################### OntoSim Batch STOP ####################");
	}

}
