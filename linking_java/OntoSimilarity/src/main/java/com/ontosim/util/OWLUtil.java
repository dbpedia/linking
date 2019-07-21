package com.ontosim.util;

import java.io.ByteArrayInputStream;
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
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;

import com.google.gson.Gson;
import com.ontosim.cnst.OntoConst;
import com.ontosim.model.OntoFileModel;
import com.ontosim.model.OntoInfoModel;
import com.ontosim.model.OntoServiceModel;

public class OWLUtil {

	public OntoInfoModel decodeFile(OntoFileModel file, OntoInfoModel ontoFlModel) throws Exception {
		Base64.Decoder dec = Base64.getDecoder();
		byte[] decbytes = dec.decode(file.getFile().replace("data:application/octet-stream;base64,", ""));
		ByteArrayInputStream in = new ByteArrayInputStream(decbytes);

		ontoFlModel.setFileNm(file.getFile_nm());
		ontoFlModel.setFileIpStream(in);

		return ontoFlModel;
	}

	public String encodeFile(File file) throws Exception {

		Base64.Encoder enc = Base64.getEncoder();
		String encodedString = enc.encodeToString(FileUtils.readFileToByteArray(file));

		return encodedString;
	}

	public OntoInfoModel initilizeOwlVar(OntoInfoModel ontoFlmodel) throws OWLOntologyCreationException {

		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		OWLOntology ontology = manager.loadOntologyFromOntologyDocument(ontoFlmodel.getFileIpStream());
		OWLReasonerFactory reasonerFactory = new ReasonerFactory();

		OWLReasoner reasoner = reasonerFactory.createReasoner(ontology);
		OWLDataFactory dataFactory = manager.getOWLDataFactory();

		ontoFlmodel.setManager(manager);
		ontoFlmodel.setOntology(ontology);
		ontoFlmodel.setDataFactory(dataFactory);
		ontoFlmodel.setReasoner(reasoner);

		return ontoFlmodel;
	}

	public OntoServiceModel convertToServiceModel(String serviceIp) throws OWLOntologyCreationException {
		Gson gson = new Gson();
		OntoServiceModel ontoServiceModel = gson.fromJson(serviceIp, OntoServiceModel.class);

		return ontoServiceModel;
	}

	public String convertFrmServiceModel(OntoServiceModel serviceOp) throws OWLOntologyCreationException {
		Gson gson = new Gson();

		return gson.toJson(serviceOp);
	}

	public byte[] loadFile(File file) throws IOException {
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
	
	public boolean isNotCls(ClassExpressionType metaInfo){
		
		if(metaInfo != ClassExpressionType.OWL_CLASS){
			return true;
		}
		
		return false;
	}
	
	public String getComplex(String str){
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
