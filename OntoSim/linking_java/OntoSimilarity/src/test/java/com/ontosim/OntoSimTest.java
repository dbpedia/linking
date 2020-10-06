package com.ontosim;

import java.io.File;
import java.text.SimpleDateFormat;
import java.time.Duration;
import java.time.Instant;
import java.util.Date;
import java.util.concurrent.TimeUnit;

import org.junit.Ignore;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.ontosim.adapter.OntoConnController;
import com.ontosim.cnst.OntoConst;
import com.ontosim.model.OntoDbModel;

/**
 * @author jaydeep
 * srcFlPath, trgtFlPath, opPath, datasourceNm
 * 
 * Anatomy > human.owl, mouse.owl
 * 
 * LargeBio-task-1 > s_oaei_FMA_small_overlapping_nci.owl, t_oaei_NCI_small_overlapping_fma.owl
 * LargeBio-task-2 > s_oaei_FMA_whole_ontology.owl, t_oaei_NCI_whole_ontology.owl
 * LargeBio-task-3 > s_oaei_FMA_small_overlapping_snomed.owl, t_oaei_SNOMED_small_overlapping_fma.owl
 * LargeBio-task-4 > s_oaei_FMA_whole_ontology.owl, t_oaei_SNOMED_extended_overlapping_fma_nci.owl
 * LargeBio-task-5 > s_oaei_SNOMED_small_overlapping_nci.owl, t_oaei_NCI_small_overlapping_snomed.owl
 * LargeBio-task-6 > s_oaei_SNOMED_extended_overlapping_fma_nci.owl, t_oaei_NCI_whole_ontology.owl
 *
 */

public class OntoSimTest {

	@Test
	@Ignore
	public void test() {

		try {
			final Logger logger = LoggerFactory.getLogger(OntoSimTest.class);

			logger.info("#################### OntoSim Batch START ####################");
			Instant start = Instant.now();
			
			try{
								
				int[] vec_arr = new int[]{100};
				int[] op_k_arr = new int[]{1};
				double[] threshold_ds_arr = new double[]{0.04};
				
				for(int vec : vec_arr){
					for(int op_k : op_k_arr){
						for(double threshold_ds : threshold_ds_arr){
							
							String ontoFlPath = System.getProperty("user.dir") + File.separator + "ontofiles/local";
							String srcFlPath = ontoFlPath + File.separator + "source.owl";
							String trgtFlPath = ontoFlPath + File.separator + "target.owl";
							
							String currTimeStamp = new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss").format(new Date());
							String resultsPath = ontoFlPath + File.separator + "result"+"-"+vec+"-"+op_k+"-"+threshold_ds+".rdf";
							
							// Calling OntoConnController
							OntoConnController ontoConnController = new OntoConnController();
							
							//Make it finalize before submit
							OntoDbModel ontoDbModel = new OntoDbModel();
							ontoDbModel.setDb_nm(OntoConst.DS_1);
							ontoDbModel.setVec_dim(vec);
							ontoDbModel.setWord_wt_ds(OntoConst.word_wt_ds);//0.5
							ontoDbModel.setMeta_wt_ds(OntoConst.meta_wt_ds);//0.5
							ontoDbModel.setOp_k(op_k);
							ontoDbModel.setThreshold_ds(threshold_ds);
							
							ontoConnController.ontoConnController(srcFlPath, trgtFlPath, resultsPath, ontoDbModel);
							
							TimeUnit.SECONDS.sleep(5);//wait for 5 seconds
							
						}
					}
				}
							
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
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

}



////// VECTOR-DIMENSION START //////
// int vec_dim = 100;
//int vec_dim = 200;
// int vec_dim = 300;
////// VECTOR-DIMENSION END //////

////// TEST PARAMETER START //////
//int op_k=5;
//int op_k=3;
//int op_k=1;

//////For Anatomy dataset (distance | similarity)
// double threshold_ds = 0.01; //0.99
// double threshold_ds = 0.02; //0.98
// double threshold_ds = 0.03; //0.97
// double threshold_ds = 0.04; //0.96
// double threshold_ds = 0.05; //0.95
// double threshold_ds = 0.06; //0.94
// double threshold_ds = 0.07; //0.93
// double threshold_ds = 0.08; //0.92
// double threshold_ds = 0.09; //0.91
// double threshold_ds = 0.10; //0.90
// double threshold_ds = 0.15; //0.85
// double threshold_ds = 0.20; //0.80
// double threshold_ds = 0.25; //0.75
// double threshold_ds = 0.30; //0.70
// double threshold_ds = 0.35; //0.65
// double threshold_ds = 0.40; //0.60
// double threshold_ds = 0.45; //0.55
// double threshold_ds = 0.50; //0.50
// double threshold_ds = 0.55; //0.45
// double threshold_ds = 0.60; //0.40
//double threshold_ds = 0.65; //0.35
// double threshold_ds = 0.70; //0.30
// double threshold_ds = 0.75; //0.25
// double threshold_ds = 0.80; //0.20
// double threshold_ds = 0.85; //0.15
// double threshold_ds = 0.90; //0.10
// double threshold_ds = 0.95; //0.05
// double threshold_ds = 1.00; //0.00
////// TEST PARAMETER START //////
