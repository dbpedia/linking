package com.ontosim.util;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Base64;

import org.apache.commons.io.FileUtils;
import org.semanticweb.HermiT.ReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.ClassExpressionType;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;

import com.google.gson.Gson;
import com.ontosim.cnst.OntoConst;
import com.ontosim.model.OntoInfoModel;
import com.ontosim.model.OntoServiceModel;

public class OWLUtil {

	public String encodeFile(File file) throws Exception {

		Base64.Encoder enc = Base64.getEncoder();
		String encodedString = enc.encodeToString(FileUtils.readFileToByteArray(file));

		return encodedString;
	}

	public OntoInfoModel initilizeOwlVar(OntoInfoModel ontoFlmodel) throws Exception {

		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		OWLOntology ontology = manager.loadOntologyFromOntologyDocument(ontoFlmodel.getFileIpStream());
		OWLReasonerFactory reasonerFactory = new ReasonerFactory();

		OWLReasoner reasoner = reasonerFactory.createReasoner(ontology);
		OWLDataFactory dataFactory = manager.getOWLDataFactory();

		ontoFlmodel.setManager(manager);
		ontoFlmodel.setOntology(ontology);
		ontoFlmodel.setDataFactory(dataFactory);
		ontoFlmodel.setReasoner(reasoner);
		
		ontoFlmodel.setFileIpStream(null);//removing input stream as that is not need anymore.

		return ontoFlmodel;
	}

	public OntoServiceModel convertToServiceModel(String serviceIp)  throws Exception {
		Gson gson = new Gson();
		OntoServiceModel ontoServiceModel = gson.fromJson(serviceIp, OntoServiceModel.class);

		return ontoServiceModel;
	}

	public String convertFrmServiceModel(OntoServiceModel serviceOp) throws Exception {
		System.out.println("convertFrmServiceModel START");
		Gson gson = new Gson();
		String serviceOpStr = gson.toJson(serviceOp);
		System.out.println("convertFrmServiceModel STOP");
		return serviceOpStr;
	}

	public byte[] loadFile(File file)  throws Exception {
		InputStream is = new FileInputStream(file);

		long length = file.length();
		if (length > Integer.MAX_VALUE) {
			// File is too large
		}
		byte[] bytes = new byte[(int) length];

		int offset = 0;
		int numRead = 0;
		while (offset < bytes.length && (numRead = is.read(bytes, offset, bytes.length - offset)) >= 0) {
			offset += numRead;
		}

		is.close();
		
		if (offset < bytes.length) {
			throw new IOException("Could not completely read file " + file.getName());
		}

		
		return bytes;
	}
	
	public boolean isNotCls(ClassExpressionType metaInfo) throws Exception{
		
		if(metaInfo != ClassExpressionType.OWL_CLASS){
			return true;
		}
		
		return false;
	}
	
	public String getComplex(String str) throws Exception {
		str = str.replace(" ", ",")
				.replace(OntoConst.OntoIntersectionOf, "")
				.replace(OntoConst.OntoUnionOff, "")
				.replace(OntoConst.OntoComplementOf, "")
				.replace(OntoConst.OntoOneOf, "")
				.replace(OntoConst.OntoSomeValuesFrom, "")
				.replace(OntoConst.OntoAllValuesFrom, "")
				.replace(OntoConst.OntoMinCardinality, "")
				.replace(OntoConst.OntoMaxCardinality, "")
				.replace(OntoConst.OntoExactCardinality, "")
				.replace(OntoConst.OntoHasValuef, "");
		
		return str;
	}
}
