package com.ontosim.service;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import com.ontosim.bl.OntoSimBL;
import com.ontosim.model.OntoFileModel;
import com.ontosim.model.OntoServiceModel;
import com.ontosim.util.OWLUtil;

@Path("v2")
public class OntoSimService {

	OWLUtil owlUtil = new OWLUtil();
	OntoSimBL ontoSimBL = new OntoSimBL();

	@POST
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	@Path("task1")
	public String parseOntoOWL(String ontoInput) {

		String retJSONStr = "";
		try {
			if("".equals(ontoInput)){
				return retJSONStr;
			}
			
			OntoServiceModel ontoServiceModel = owlUtil.convertToServiceModel(ontoInput);

			String srcBase64_Fl = ontoSimBL.ontoSimBL(ontoServiceModel.getSrc_in_data());
			OntoFileModel src_op_data = new OntoFileModel();
			src_op_data.setFile(srcBase64_Fl);
			src_op_data.setFile_nm("source.json");
			src_op_data.setFile_typ("application/json");
			ontoServiceModel.setSrc_op_data(src_op_data);

			String trgtBase64_Fl = ontoSimBL.ontoSimBL(ontoServiceModel.getTrgt_in_data());
			OntoFileModel trgt_op_data = new OntoFileModel();
			trgt_op_data.setFile(trgtBase64_Fl);
			trgt_op_data.setFile_nm("target.json");
			trgt_op_data.setFile_typ("application/json");
			ontoServiceModel.setTrgt_op_data(trgt_op_data);

			retJSONStr = owlUtil.convertFrmServiceModel(ontoServiceModel);

		} catch (Exception e) {
			e.printStackTrace();
		}

		return retJSONStr;
	}
	
	@GET
	@Path("health")
	public String testWebService() {
		return "Ontosim : java web service is working!";
	}

}
