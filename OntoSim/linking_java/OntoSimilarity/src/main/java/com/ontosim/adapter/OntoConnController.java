package com.ontosim.adapter;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Base64;

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.Gson;
import com.ontosim.bl.OntoSimBL;
import com.ontosim.cnst.OntoConst;
import com.ontosim.model.OntoDbModel;
import com.ontosim.model.OntoFileModel;
import com.ontosim.model.OntoServiceModel;
import com.ontosim.util.OWLUtil;
import com.ontosim.util.OntoCallReqUtil;

public class OntoConnController {

	OntoSimBL ontoSimBL = new OntoSimBL();
	OWLUtil owlUtil = new OWLUtil();
	OntoCallReqUtil ontoCallReqUtil = new OntoCallReqUtil();
	Gson gson = new Gson();
	Base64.Decoder dec = Base64.getDecoder();
	private static final Logger logger = LoggerFactory.getLogger(OntoConnController.class);
	
	
	

	public void ontoConnController(String srcFlPath, String trgtFlPath, String opFlPath, OntoDbModel ontoDbModel) throws Exception {

		logger.info("#################### ontoConnController START ####################");		
		
		File srcFl = new File(srcFlPath);
		File trgtFl = new File(trgtFlPath);		

		OntoServiceModel ontoServiceModel = new OntoServiceModel();
		ontoServiceModel.setDb(ontoDbModel);
		
		logger.info("SOURCE file computing - ontoSimBL");
		// Source file
		InputStream srcFlIn = new FileInputStream(srcFl);
		String srcBase64_Fl = ontoSimBL.ontoSimBL(srcFlIn, OntoConst.SRC);
		OntoFileModel src_in_data = new OntoFileModel();
		src_in_data.setFile(srcBase64_Fl);
		src_in_data.setFile_nm(OntoConst.SRC_FL);
		src_in_data.setFile_typ(OntoConst.FL_TYP);
		ontoServiceModel.setSrc_in_data(src_in_data);
		
		logger.info("TARGET file computing - ontoSimBL");
		// target file
		InputStream trgtFlIn = new FileInputStream(trgtFl);
		String trgtBase64_Fl = ontoSimBL.ontoSimBL(trgtFlIn, OntoConst.TRGT);
		OntoFileModel trgt_in_data = new OntoFileModel();
		trgt_in_data.setFile(trgtBase64_Fl);
		trgt_in_data.setFile_nm(OntoConst.TRGT_FL);
		trgt_in_data.setFile_typ(OntoConst.FL_TYP);
		ontoServiceModel.setTrgt_in_data(trgt_in_data);

		logger.info("GENERATING INPUT SERVICE MODEL - convertFrmServiceModel");
		String retJSONStr = owlUtil.convertFrmServiceModel(ontoServiceModel);
		
		logger.info("CALLING PYTHON SERVICE - ontoPOSTRequest");
		String finalRetJSONStr = ontoCallReqUtil.ontoPOSTRequest(OntoConst.PY_SERVICE_URL, retJSONStr);

		logger.info("GENERATING OUTPUT SERVICE MODEL - convertFrmServiceModel");
		Gson gson = new Gson();
		OntoServiceModel finalOntoServiceModel = gson.fromJson(finalRetJSONStr, OntoServiceModel.class);
		
		logger.info("WRITING  output START");
		logger.info(opFlPath);
		File opfile = new File(opFlPath);
		byte[] decbytes = dec.decode(finalOntoServiceModel.getFinal_op_data().getFile());
		FileUtils.writeByteArrayToFile( opfile, decbytes );
		logger.info("WRITING output END");
		
		logger.info("#################### ontoConnController STOP ####################");
		
	}
	
}
