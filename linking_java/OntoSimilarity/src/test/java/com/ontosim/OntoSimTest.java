package com.ontosim;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;

import org.apache.commons.codec.binary.Base64;
import org.apache.commons.io.IOUtils;
import org.junit.Test;

import com.google.gson.Gson;
import com.ontosim.model.OntoFileModel;
import com.ontosim.model.OntoServiceModel;
import com.ontosim.service.OntoSimService;

public class OntoSimTest {

	OntoSimService ontoSimService = new OntoSimService();
	
	@Test
	public void test() {
		
		try{
			
			String srcFlPath = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/2018/KnowledgeGraphs/LargeBio_dataset_oaei2019/local_Gen/task_1_NCI_FMA/oaei_NCI_whole_ontology.owl";
			String trgtFlPath = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/2018/KnowledgeGraphs/LargeBio_dataset_oaei2019/local_Gen/task_1_NCI_FMA/oaei_FMA_small_overlapping_nci.owl";
			
			File srcFile = new File(srcFlPath);
			InputStream srcIs = new FileInputStream(srcFile);
			byte[] srcBytes = IOUtils.toByteArray(srcIs);
			String srcStr = Base64.encodeBase64String(srcBytes);
			
			File trgtFile = new File(trgtFlPath);
			InputStream trgtIs = new FileInputStream(trgtFile);
			byte[] trgtBytes = IOUtils.toByteArray(trgtIs);
			String trgtStr = Base64.encodeBase64String(trgtBytes);
			
			//Input source file
			OntoFileModel ontoFileModelSrcIn = new OntoFileModel();
			ontoFileModelSrcIn.setAvailable(true);
			ontoFileModelSrcIn.setFile_nm("oaei_NCI_whole_ontology.owl");
			ontoFileModelSrcIn.setFile_typ("");
			ontoFileModelSrcIn.setFile(srcStr);
			
			//Input target file
			OntoFileModel ontoFileModelTrgtIn = new OntoFileModel();
			ontoFileModelTrgtIn.setAvailable(true);
			ontoFileModelTrgtIn.setFile_nm("oaei_FMA_small_overlapping_nci.owl");
			ontoFileModelTrgtIn.setFile_typ("");
			ontoFileModelTrgtIn.setFile(trgtStr);
			
			
			//Output source file
			OntoFileModel ontoFileModelSrcOp = new OntoFileModel();
			ontoFileModelSrcOp.setAvailable(false);
			ontoFileModelSrcOp.setFile_nm("");
			ontoFileModelSrcOp.setFile_typ("");
			ontoFileModelSrcOp.setFile(null);

			
			//Output target file
			OntoFileModel ontoFileModelTrgtOp = new OntoFileModel();
			ontoFileModelTrgtOp.setAvailable(false);
			ontoFileModelTrgtOp.setFile_nm("");
			ontoFileModelTrgtOp.setFile_typ("");
			ontoFileModelTrgtOp.setFile(null);
			
			
			OntoServiceModel ontoServiceModelObj = new OntoServiceModel();
			ontoServiceModelObj.setSrc_in_data(ontoFileModelSrcIn);
			ontoServiceModelObj.setTrgt_in_data(ontoFileModelTrgtIn);
			ontoServiceModelObj.setSrc_op_data(ontoFileModelSrcOp);
			ontoServiceModelObj.setTrgt_op_data(ontoFileModelTrgtOp);
			
			
			Gson gson = new Gson();
			String ontoSimJsonIp = gson.toJson(ontoServiceModelObj);
			
			
			String ontoSimJsonOp = ontoSimService.parseOntoOWL(ontoSimJsonIp);
			
			
			OntoServiceModel ontoServiceModel = gson.fromJson(ontoSimJsonOp, OntoServiceModel.class);
			
			byte[] srcDecodedOp = Base64.decodeBase64(ontoServiceModel.getSrc_op_data().getFile());
			String srcFileDest = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/2018/KnowledgeGraphs/LargeBio_dataset_oaei2019/local_Gen/task_1_NCI_FMA/source.json";
			FileOutputStream srcFileOuputStream = new FileOutputStream(srcFileDest);
			srcFileOuputStream.write(srcDecodedOp);
			srcFileOuputStream.close();
			
			byte[] trgtDecodedOp = Base64.decodeBase64(ontoServiceModel.getTrgt_op_data().getFile());
			String trgtFileDest = "/Users/jaydeep/jaydeep_workstation/ASU/Research/oaei/2018/KnowledgeGraphs/LargeBio_dataset_oaei2019/local_Gen/task_1_NCI_FMA/target.json";
			FileOutputStream trgtFileOuputStream = new FileOutputStream(trgtFileDest);
			trgtFileOuputStream.write(trgtDecodedOp);
			trgtFileOuputStream.close();
			
			System.out.println("DONE");
			
		}catch(Exception e){
			e.printStackTrace();
		}
		
		
	}
	
	

}
