package com.ontosim.service;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import org.codehaus.plexus.util.ExceptionUtils;

import com.ontosim.bl.OntoSimBL;
import com.ontosim.cnst.OntoConst;
import com.ontosim.exception.OntoException;
import com.ontosim.model.OntoFileModel;
import com.ontosim.model.OntoFileMsg;
import com.ontosim.model.OntoServiceModel;
import com.ontosim.util.OWLUtil;

@Path("ontojava")
public class OntoSimService {

	OWLUtil owlUtil = new OWLUtil();
	OntoSimBL ontoSimBL = new OntoSimBL();

	@POST
	@Consumes(MediaType.APPLICATION_JSON)
	@Produces(MediaType.APPLICATION_JSON)
	@Path("task1")
	public String ontoJavaMtdh(String ontoInput) {
		System.out.println("#################### Java OWL API START ####################");
		String retJSONStr = "";
		try {
			if ("".equals(ontoInput)) {
				throw new OntoException(OntoConst.ERR_MSG_1);
			}

			OntoServiceModel ontoServiceModel = owlUtil.convertToServiceModel(ontoInput);

			if (ontoServiceModel.getSrc_in_data().getFile() == null) {
				throw new OntoException(OntoConst.ERR_MSG_2);
			}

			if (ontoServiceModel.getTrgt_in_data().getFile() == null) {
				throw new OntoException(OntoConst.ERR_MSG_3);
			}

			String srcBase64_Fl = ontoSimBL.ontoSimBL(ontoServiceModel.getSrc_in_data(), OntoConst.SRC);
			OntoFileModel src_in_data = new OntoFileModel();
			src_in_data.setFile(srcBase64_Fl);
			src_in_data.setFile_nm(OntoConst.SRC_FL);
			src_in_data.setFile_typ(OntoConst.FL_TYP);
			ontoServiceModel.setSrc_in_data(src_in_data);

			String trgtBase64_Fl = ontoSimBL.ontoSimBL(ontoServiceModel.getTrgt_in_data(), OntoConst.TRGT);
			OntoFileModel trgt_in_data = new OntoFileModel();
			trgt_in_data.setFile(trgtBase64_Fl);
			trgt_in_data.setFile_nm(OntoConst.TRGT_FL);
			trgt_in_data.setFile_typ(OntoConst.FL_TYP);
			ontoServiceModel.setTrgt_in_data(trgt_in_data);

			retJSONStr = owlUtil.convertFrmServiceModel(ontoServiceModel);

		} catch (Exception e) {
			OntoServiceModel ontoServiceModel = new OntoServiceModel();
			OntoFileMsg ontoFileMsg = new OntoFileMsg();
			ontoFileMsg.setMsg_val(OntoConst.ERR);
			ontoFileMsg.setMsg_cause(ExceptionUtils.getFullStackTrace(e));
			ontoServiceModel.setMsg(ontoFileMsg);
			try {
				retJSONStr = owlUtil.convertFrmServiceModel(ontoServiceModel);
			} catch (Exception e1) {
				// This should never happen, should be tested
				e1.printStackTrace();
			}
		} finally {
			System.out.println("#################### Java OWL API STOP ####################");
		}

		return retJSONStr;
	}

	@GET
	@Path("testtask")
	public String testWebService() {
		return "Ontosim : java web service is working!";
	}

}
