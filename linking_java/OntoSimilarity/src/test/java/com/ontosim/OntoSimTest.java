package com.ontosim;

import java.io.File;
import java.util.Base64;

import org.apache.commons.io.FileUtils;
import org.junit.Test;

import com.google.gson.Gson;
import com.ontosim.model.OntoFileModel;
import com.ontosim.model.OntoServiceModel;
import com.ontosim.service.OntoSimService;

public class OntoSimTest {

	OntoSimService ontoSimService = new OntoSimService();

	@Test
	public void test() {

		try {

//			String basePath = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/2018/KnowledgeGraphs/LargeBio_dataset_oaei2019/local_Gen/task_1_NCI_FMA/";
			String basePath = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/2018/KnowledgeGraphs/anatomy-dataset/";
			
//			String srcFlPath = basePath + "oaei_NCI_whole_ontology.owl";
//			String trgtFlPath = basePath + "oaei_FMA_small_overlapping_nci.owl";

			String srcFlPath = basePath + "human.owl";
			String trgtFlPath = basePath + "mouse.owl";
			
			Base64.Encoder enc = Base64.getEncoder();
			
			File srcFile = new File(srcFlPath);
			String srcStr = enc.encodeToString(FileUtils.readFileToByteArray(srcFile));

			File trgtFile = new File(trgtFlPath);
			String trgtStr = enc.encodeToString(FileUtils.readFileToByteArray(trgtFile));

			// Input source file
			OntoFileModel ontoFileModelSrcIn = new OntoFileModel();
			ontoFileModelSrcIn.setAvailable(true);
			ontoFileModelSrcIn.setFile_nm("source");
			ontoFileModelSrcIn.setFile_typ("");
			ontoFileModelSrcIn.setFile(srcStr);

			// Input target file
			OntoFileModel ontoFileModelTrgtIn = new OntoFileModel();
			ontoFileModelTrgtIn.setAvailable(true);
			ontoFileModelTrgtIn.setFile_nm("target");
			ontoFileModelTrgtIn.setFile_typ("");
			ontoFileModelTrgtIn.setFile(trgtStr);

			OntoServiceModel ontoServiceModelObj = new OntoServiceModel();
			ontoServiceModelObj.setSrc_in_data(ontoFileModelSrcIn);
			ontoServiceModelObj.setTrgt_in_data(ontoFileModelTrgtIn);

			Gson gson = new Gson();
			String ontoSimJsonIp = gson.toJson(ontoServiceModelObj);

			String ontoSimJsonOp = ontoSimService.ontoJavaMtdh(ontoSimJsonIp);

			OntoServiceModel ontoServiceModel = gson.fromJson(ontoSimJsonOp, OntoServiceModel.class);

			if (ontoServiceModel.getMsg() != null) {
				System.out.println("Error Message:- "+ontoServiceModel.getMsg().getMsg_val());
				System.out.println("Error Cause:- "+ontoServiceModel.getMsg().getMsg_cause());
			}
			
			//Save the json data in eclipse folder
			String opPath = "/Users/jaydeep/jaydeep_workstation/Workplace/Python/OntoSimilarity_GSOC_local/py_files/OntoSimPY/ontodata/eclipse/"; 
			
			File srcfile = new File( opPath + "source.json" );
			byte[] srcbytes = org.apache.commons.codec.binary.Base64.decodeBase64(ontoServiceModel.getSrc_in_data().getFile());
			FileUtils.writeByteArrayToFile( srcfile, srcbytes );
			
			File trgtfile = new File( opPath + "target.json" );
			byte[] trgtbytes = org.apache.commons.codec.binary.Base64.decodeBase64(ontoServiceModel.getTrgt_in_data().getFile());
			FileUtils.writeByteArrayToFile( trgtfile, trgtbytes );
			
			
			System.out.println("DONE");

		} catch (Exception e) {
			e.printStackTrace();
		}

	}

}
