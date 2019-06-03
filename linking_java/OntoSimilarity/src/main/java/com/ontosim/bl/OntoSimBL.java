package com.ontosim.bl;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.apache.commons.fileupload.FileItem;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLAnnotation;
import org.semanticweb.owlapi.model.OWLAnnotationValue;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassAxiom;
import org.semanticweb.owlapi.model.OWLClassExpression;
import org.semanticweb.owlapi.model.OWLLiteral;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.model.OWLObjectSomeValuesFrom;
import org.semanticweb.owlapi.model.OWLObjectVisitor;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLQuantifiedObjectRestriction;
import org.semanticweb.owlapi.model.OWLSubClassOfAxiom;
import org.semanticweb.owlapi.search.EntitySearcher;

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ontosim.model.OntoFileModel;
import com.ontosim.model.OntoSimClsModel;
import com.ontosim.model.OntoSimObjPropModel;
import com.ontosim.model.OntoSimRelModel;
import com.ontosim.util.FileUploadUtil;
import com.ontosim.util.OWLUtil;

public class OntoSimBL {

	FileUploadUtil fileUploadUtl = new FileUploadUtil();
	OWLUtil owlUtil = new OWLUtil();

	public List<File> ontoSimBL(FileItem item) throws Exception {

		/**
		 * Creating Variables
		 */
		List<File> retFileLst = new ArrayList<File>();
		OntoFileModel ontoFileModel = new OntoFileModel();
		Map<String, OntoSimClsModel> ontoClsMap = new HashMap<String, OntoSimClsModel>(); // only
																							// for
																							// classes
		// Map<String, OntoSimClsModel> ontoClsMap = new HashMap<String,
		// OntoSimClsModel>(); //only for Individuals
		Map<String, OntoSimObjPropModel> ontoObjPropsMap = new HashMap<String, OntoSimObjPropModel>(); // only
																										// for
																										// Object
																										// Properties
		// Map<String, OntoSimClsModel> ontoClsMap = new HashMap<String,
		// OntoSimClsModel>(); //only for Data Properties
		// Map<String, OntoSimClsModel> ontoClsMap = new HashMap<String,
		// OntoSimClsModel>(); //only for Annotation Properties
		Map<String, OntoSimRelModel> ontoSimRelMap = new HashMap<String, OntoSimRelModel>(); // only
																								// for
																								// Relation

		/**
		 * 1) It saves the .owl file as InputStream in ontoFileModel
		 */
		this.uploadFile(item, ontoFileModel);

		/**
		 * 2) Initialize owl variables in ontoFileModel
		 */
		this.initilizeOwlVar(ontoFileModel);

		/**
		 * 3) populate Class Information
		 */
		this.populateClsVals(ontoFileModel, ontoClsMap);

		/**
		 * 4) Write the Class output into json file and download
		 */
		retFileLst.add(this.writeJson(item.getFieldName() + ".json", ontoClsMap));

		/**
		 * 5) populate Object Property Information
		 */
		this.populateObjPropsVals(ontoFileModel, ontoObjPropsMap);

		/**
		 * 6) Write the Object Property output into json file and download
		 */
		retFileLst.add(this.writeJson(item.getFieldName() + "_ObjProp.json", ontoObjPropsMap));

		/**
		 * 7) populate Relation Information
		 */
		this.populateRelVals(ontoSimRelMap);

		/**
		 * 8) Write the Relation output into json file and download
		 */
		retFileLst.add(this.writeJson(item.getFieldName() + "_Rel.json", ontoSimRelMap));

		return retFileLst;

	}

	private void populateObjPropsVals(OntoFileModel ontoFileModel, Map<String, OntoSimObjPropModel> ontoObjPropsMap) {

		Stream<OWLObjectProperty> allObjProps = ontoFileModel.getOntology().objectPropertiesInSignature();
		allObjProps.forEach(objProp -> {

			Set<OWLAnnotation> annoLst = EntitySearcher
					.getAnnotations(objProp, ontoFileModel.getOntology(), ontoFileModel.getDataFactory().getRDFSLabel())
					.collect(Collectors.toSet());
			OntoSimObjPropModel ontoSimObjPropModel = new OntoSimObjPropModel();
			for (OWLAnnotation anno : annoLst) {
				OWLAnnotationValue val = anno.getValue();
				if (val instanceof OWLLiteral) {
					String value = ((OWLLiteral) val).getLiteral();
					ontoSimObjPropModel.setIri(objProp.toString());
					ontoSimObjPropModel.setLbl(value);
				}
			}

			ontoObjPropsMap.put(objProp.toString(), ontoSimObjPropModel);
		});
	}

	private void populateRelVals(Map<String, OntoSimRelModel> ontoObjPropsMap) {

		OntoSimRelModel ontoSimParent = new OntoSimRelModel();
		String ontoSimParentIri = "<http://ontosim.owl#ontoparent>";
		ontoSimParent.setIri(ontoSimParentIri);
		ontoSimParent.setLbl("parent");
		ontoObjPropsMap.put(ontoSimParentIri, ontoSimParent);
		
		OntoSimRelModel ontoSimChild = new OntoSimRelModel();
		String ontoSimChildIri = "<http://ontosim.owl#ontochild>";
		ontoSimChild.setIri(ontoSimChildIri);
		ontoSimChild.setLbl("child");
		ontoObjPropsMap.put(ontoSimChildIri, ontoSimChild);
		
		OntoSimRelModel ontoSimEqCls = new OntoSimRelModel();
		String ontoSimEqClsIri = "<http://ontosim.owl#ontoeqcls>";
		ontoSimEqCls.setIri(ontoSimEqClsIri);
		ontoSimEqCls.setLbl("equivalent");
		ontoObjPropsMap.put(ontoSimEqClsIri, ontoSimEqCls);
		
		OntoSimRelModel ontoSimDisjCls = new OntoSimRelModel();
		String ontoSimDisjClsIri = "<http://ontosim.owl#ontodisjcls>";
		ontoSimDisjCls.setIri(ontoSimDisjClsIri);
		ontoSimDisjCls.setLbl("disjoint");
		ontoObjPropsMap.put(ontoSimDisjClsIri, ontoSimDisjCls);

		
		OntoSimRelModel ontoSimRelCls = new OntoSimRelModel();
		String ontoSimRelClsIri = "<http://ontosim.owl#ontores>";
		ontoSimRelCls.setIri(ontoSimRelClsIri);
		ontoSimRelCls.setLbl("restriction");
		ontoObjPropsMap.put(ontoSimRelClsIri, ontoSimRelCls);
		
	}

	private void populateClsVals(OntoFileModel ontoFileModel, Map<String, OntoSimClsModel> ontoClsMap) {

		/**
		 * 1) All concepts - rdfs:labels are loaded in ontoMap
		 */
		this.getAllConceptsWithLabels(ontoFileModel, ontoClsMap);

		/**
		 * 2) All the hierarchy details will be populated
		 */
		this.getHierarchyDtls(ontoFileModel, ontoClsMap);

		/**
		 * 3) All the disjoint classes will be loaded
		 */
		this.getDisjointCls(ontoFileModel, ontoClsMap);

		/**
		 * 4) All the equivalent classes will be loaded
		 */
		this.getEqCls(ontoFileModel, ontoClsMap);

		/**
		 * 5) All the restrictions will be loaded
		 */
		this.getRestriction(ontoFileModel, ontoClsMap);

	}

	private OntoFileModel uploadFile(FileItem item, OntoFileModel ontoFlModel) throws Exception {

		return fileUploadUtl.uploadFile(item, ontoFlModel);

	}

	private OntoFileModel initilizeOwlVar(OntoFileModel ontoFileModel) throws OWLOntologyCreationException {

		return owlUtil.initilizeOwlVar(ontoFileModel);
	}

	private void getAllConceptsWithLabels(OntoFileModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) {

		Stream<OWLClass> allClasses = ontoFileModel.getOntology().classesInSignature();
		allClasses.forEach(clazz -> {

			Set<OWLAnnotation> annoLst = EntitySearcher
					.getAnnotations(clazz, ontoFileModel.getOntology(), ontoFileModel.getDataFactory().getRDFSLabel())
					.collect(Collectors.toSet());
			String key = clazz.getIRI().toString();

			for (OWLAnnotation anno : annoLst) {
				OWLAnnotationValue val = anno.getValue();
				if (val instanceof OWLLiteral) {
					String value = ((OWLLiteral) val).getLiteral();
					OntoSimClsModel ontoSim = new OntoSimClsModel();
					ontoSim.setIri(key);
					ontoSim.setLbl(value);

					ontoMap.put(key, ontoSim);
				}
			}
		});
	}

	public void getHierarchyDtls(OntoFileModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) {

		// For direct hierarchy(immediate parent and child)
		for (String key : ontoMap.keySet()) {
			OWLClass claz = ontoFileModel.getDataFactory().getOWLClass(IRI.create(key));
			List<String> parents = new ArrayList<String>();
			List<OWLClass> supCls = ontoFileModel.getReasoner().getSuperClasses(claz, true).entities()
					.collect(Collectors.toList());

			for (OWLClass parent : supCls) {
				String parentVal = parent.getIRI().toString();
				parents.add(parentVal);
			}
			ontoMap.get(key).setParentCls(parents);

			List<String> children = new ArrayList<String>();
			List<OWLClass> subCls = ontoFileModel.getReasoner().getSubClasses(claz, true).entities()
					.collect(Collectors.toList());

			for (OWLClass child : subCls) {
				String childVal = child.getIRI().toString();
				children.add(childVal);
			}
			ontoMap.get(key).setChildCls(children);

		}
	}

	private void getDisjointCls(OntoFileModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) {

		for (String key : ontoMap.keySet()) {
			OWLClass outerClaz = ontoFileModel.getDataFactory().getOWLClass(IRI.create(key));

			Iterator<OWLClassExpression> disjntItr = EntitySearcher
					.getDisjointClasses(outerClaz, ontoFileModel.getOntology()).iterator();
			List<String> strLst = new ArrayList<String>();

			while (disjntItr.hasNext()) {
				String disjntVal = disjntItr.next().toString();
				// <http://human.owl#NCI_C25444>
				// this is to remove < and > from the value
				disjntVal = disjntVal.substring(1, disjntVal.length() - 1);
				if (!disjntVal.equals(key)) {
					strLst.add(disjntVal);
				}
			}
			ontoMap.get(key).setDisjointCls(strLst);
		}
	}

	private void getEqCls(OntoFileModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) {

		for (String key : ontoMap.keySet()) {
			OWLClass outerClaz = ontoFileModel.getDataFactory().getOWLClass(IRI.create(key));

			Iterator<OWLClassExpression> eqItr = EntitySearcher
					.getEquivalentClasses(outerClaz, ontoFileModel.getOntology()).iterator();
			List<String> strLst = new ArrayList<String>();

			while (eqItr.hasNext()) {
				String eqVal = eqItr.next().toString();
				// <http://human.owl#NCI_C25444>
				// this is to remove < and > from the value
				eqVal = eqVal.substring(1, eqVal.length() - 1);
				if (!eqVal.equals(key)) {
					strLst.add(eqVal);
				}
			}
			ontoMap.get(key).setEqCls(strLst);

		}

	}

	// https://tutorial-academy.com/owlapi-5-read-class-restriction-axiom-visitor/
	// https://stackoverflow.com/questions/46170981/retrieve-owl-class-restrictions-using-owl-api
	// https://owlcs.github.io/owlapi/apidocs_4/org/semanticweb/owlapi/model/ClassExpressionType.html
	// https://github.com/owlcollab/owltools/blob/master/OWLTools-Core/src/main/java/owltools/mooncat/Mooncat.java
	// https://stackoverflow.com/questions/47980787/getting-object-properties-and-classes
	// https://stackoverflow.com/questions/28968495/retrieve-owlrestrictions-using-the-owl-api
	private void getRestriction(OntoFileModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) {

		for (String key : ontoMap.keySet()) {
			Map<String, List<String>> restrictionMap = new HashMap<String, List<String>>();
			OWLClass claz = ontoFileModel.getDataFactory().getOWLClass(IRI.create(key));
			Iterator<OWLClassAxiom> resItr = ontoFileModel.getOntology().axioms(claz).iterator();
			while (resItr.hasNext()) {
				OWLClassAxiom ocaxiom = resItr.next();
				// create an object visitor to get to the subClass restrictions
				ocaxiom.accept(new OWLObjectVisitor() {
					// found the subClassOf axiom
					public void visit(OWLSubClassOfAxiom subClassAxiom) {
						// create an object visitor to read the underlying
						// (subClassOf) restrictions
						subClassAxiom.getSuperClass().accept(new OWLObjectVisitor() {
							public void visit(OWLObjectSomeValuesFrom someValuesFromAxiom) {
								printQuantifiedRestriction(someValuesFromAxiom, restrictionMap);
							}
						});
					}
				});
			}
			ontoMap.get(key).setRestriction(restrictionMap);
		}
	}

	// Example
	// http://human.owl#NCI_C32546
	// ClassExpressionType: ObjectSomeValuesFrom
	// #restriction.getClassExpressionType().toString()
	// Property: <http://human.owl#UNDEFINED_part_of>
	// #restriction.getProperty().toString()
	// Object: <http://human.owl#NCI_C12393> #restriction.getFiller().toString()

	public void printQuantifiedRestriction(OWLQuantifiedObjectRestriction restriction,
			Map<String, List<String>> restrictionMap) {
		String prop = restriction.getProperty().toString();
		String obj = restriction.getFiller().toString();
		// <http://human.owl#NCI_C25444>
		// this is to remove < and > from the value
		obj = obj.substring(1, obj.length() - 1);
		if (restrictionMap.containsKey(prop)) {
			restrictionMap.get(prop).add(obj);
		} else {
			List<String> objLst = new ArrayList<String>();
			objLst.add(obj);
			restrictionMap.put(prop, objLst);
		}
	}

	public File writeJson(String fl_nm, Object ontoMap)
			throws JsonGenerationException, JsonMappingException, IOException {

		File file = new File(fl_nm);
		ObjectMapper mapper = new ObjectMapper();
		mapper.writerWithDefaultPrettyPrinter().writeValue(file, ontoMap);
		return file;
	}

}
