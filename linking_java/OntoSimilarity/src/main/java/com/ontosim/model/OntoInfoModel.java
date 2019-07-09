package com.ontosim.model;

import java.io.InputStream;

import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.reasoner.OWLReasoner;

public class OntoInfoModel {

	private String fileNm;
	private InputStream fileIpStream;
	private OWLOntologyManager manager;
	private OWLReasoner reasoner;
	private OWLOntology ontology;
	private OWLDataFactory dataFactory;
	
	public String getFileNm() {
		return fileNm;
	}
	public void setFileNm(String fileNm) {
		this.fileNm = fileNm;
	}
	public InputStream getFileIpStream() {
		return fileIpStream;
	}
	public void setFileIpStream(InputStream fileIpStream) {
		this.fileIpStream = fileIpStream;
	}
	public OWLOntologyManager getManager() {
		return manager;
	}
	public void setManager(OWLOntologyManager manager) {
		this.manager = manager;
	}
	public OWLReasoner getReasoner() {
		return reasoner;
	}
	public void setReasoner(OWLReasoner reasoner) {
		this.reasoner = reasoner;
	}
	public OWLOntology getOntology() {
		return ontology;
	}
	public void setOntology(OWLOntology ontology) {
		this.ontology = ontology;
	}
	public OWLDataFactory getDataFactory() {
		return dataFactory;
	}
	public void setDataFactory(OWLDataFactory dataFactory) {
		this.dataFactory = dataFactory;
	}
	
	
}
