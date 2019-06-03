package com.ontosim.util;

import org.semanticweb.HermiT.ReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;

import com.ontosim.model.OntoFileModel;

public class OWLUtil {


	public OntoFileModel initilizeOwlVar(OntoFileModel ontoFlmodel) throws OWLOntologyCreationException {
		
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
}
