package com.ontosim.bl;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLAnnotation;
import org.semanticweb.owlapi.model.OWLAnnotationValue;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassAxiom;
import org.semanticweb.owlapi.model.OWLClassExpression;
import org.semanticweb.owlapi.model.OWLDataHasValue;
import org.semanticweb.owlapi.model.OWLDataProperty;
import org.semanticweb.owlapi.model.OWLLiteral;
import org.semanticweb.owlapi.model.OWLObjectCardinalityRestriction;
import org.semanticweb.owlapi.model.OWLObjectExactCardinality;
import org.semanticweb.owlapi.model.OWLObjectMaxCardinality;
import org.semanticweb.owlapi.model.OWLObjectMinCardinality;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.model.OWLObjectSomeValuesFrom;
import org.semanticweb.owlapi.model.OWLObjectVisitor;
import org.semanticweb.owlapi.model.OWLQuantifiedObjectRestriction;
import org.semanticweb.owlapi.model.OWLSubClassOfAxiom;
import org.semanticweb.owlapi.search.EntitySearcher;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ontosim.cnst.OntoConst;
import com.ontosim.model.OntoFileModel;
import com.ontosim.model.OntoInfoModel;
import com.ontosim.model.OntoSimClsModel;
import com.ontosim.util.OWLUtil;

public class OntoSimBL {

	OWLUtil owlUtil = new OWLUtil();

	public String ontoSimBL(OntoFileModel file, String flNm) throws Exception {

		/**
		 * Creating Variables
		 */
		OntoInfoModel ontoFileModel = new OntoInfoModel();
		Map<String, OntoSimClsModel> ontoClsMap = new HashMap<String, OntoSimClsModel>(); // only
																							// for
																							// classes
		/**
		 * 1) It saves the .owl file as InputStream in ontoFileModel
		 */
		this.decodeFile(file, ontoFileModel);

		/**
		 * 2) Initialize owl variables in ontoFileModel
		 */
		this.initilizeOwlVar(ontoFileModel);

		/**
		 * 3) populate Class Information
		 */
		this.populateClsVals(ontoFileModel, ontoClsMap);

		/**
		 * 3) populate Class Information
		 */
		this.getObjProps(ontoFileModel, ontoClsMap);

		/**
		 * 3) populate Class Information
		 */
		this.getDataProps(ontoFileModel, ontoClsMap);

		/**
		 * 4) Write the Class output into json file and download
		 */
		File retFile = this.writeJson(flNm + OntoConst.FL_EXT, ontoClsMap);

		/**
		 * 5) Convert File to String
		 */
		String retFlStr = this.encodeFile(retFile);

		/**
		 * 6) Delete File
		 */
		this.delFl(retFile);

		return retFlStr;

	}

	private void populateClsVals(OntoInfoModel ontoFileModel, Map<String, OntoSimClsModel> ontoClsMap)
			throws Exception {

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

	private OntoInfoModel decodeFile(OntoFileModel file, OntoInfoModel ontoFlModel) throws Exception {

		return owlUtil.decodeFile(file, ontoFlModel);

	}

	private String encodeFile(File file) throws Exception {

		return owlUtil.encodeFile(file);

	}

	private void delFl(File file) throws Exception {
		file.delete();
	}

	private OntoInfoModel initilizeOwlVar(OntoInfoModel ontoFileModel) throws Exception {

		return owlUtil.initilizeOwlVar(ontoFileModel);
	}

	private void getAllConceptsWithLabels(OntoInfoModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap)
			throws Exception {

		Stream<OWLClass> allClasses = ontoFileModel.getOntology().classesInSignature();
		allClasses.forEach(clazz -> {

			Set<OWLAnnotation> annoLst = EntitySearcher
					.getAnnotations(clazz, ontoFileModel.getOntology(), ontoFileModel.getDataFactory().getRDFSLabel())
					.collect(Collectors.toSet());
			String key = clazz.getIRI().toString();
			String lbl = "";
			for (OWLAnnotation anno : annoLst) {
				OWLAnnotationValue val = anno.getValue();
				if (val instanceof OWLLiteral) {
					String value = ((OWLLiteral) val).getLiteral();
					lbl = lbl + " " + value;
				}
			}
			OntoSimClsModel ontoSim = new OntoSimClsModel();
			ontoSim.setIri(key);
			ontoSim.setLbl(lbl);
			ontoSim.setEntityTyp(OntoConst.CLS_TYP);
			ontoMap.put(key, ontoSim);
		});

	}

	public void getHierarchyDtls(OntoInfoModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) throws Exception {

		// For direct hierarchy(immediate parent and child)
		for (String key : ontoMap.keySet()) {
			OWLClass claz = ontoFileModel.getDataFactory().getOWLClass(IRI.create(key));
			List<String> parents = new ArrayList<String>();
			List<OWLClass> supCls = ontoFileModel.getReasoner().getSuperClasses(claz, true).entities()
					.collect(Collectors.toList());

			for (OWLClass parent : supCls) {
				String parentVal = parent.getIRI().toString();
				if (!(OntoConst.OntoThngCnst.equals(parentVal) || OntoConst.OntoNoThngCnst.equals(parentVal))) {
					parents.add(parentVal);
				}
			}
			ontoMap.get(key).setParentCls(parents);

			List<String> children = new ArrayList<String>();
			List<OWLClass> subCls = ontoFileModel.getReasoner().getSubClasses(claz, true).entities()
					.collect(Collectors.toList());

			for (OWLClass child : subCls) {
				String childVal = child.getIRI().toString();
				if (!(OntoConst.OntoThngCnst.equals(childVal) || OntoConst.OntoNoThngCnst.equals(childVal))) {
					children.add(childVal);
				}
			}
			ontoMap.get(key).setChildCls(children);

		}
	}

	private void getDisjointCls(OntoInfoModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) throws Exception {

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
					if (!(OntoConst.OntoThngCnst.equals(disjntVal) || OntoConst.OntoNoThngCnst.equals(disjntVal))) {
						strLst.add(disjntVal);
					}
				}
			}
			ontoMap.get(key).setDisjointCls(strLst);
		}

		// parent details is populated before
		// outside of the for loop confirms that each class has disjoint
		// classes.
		// so every parent class should have disjoint class information
		for (String key : ontoMap.keySet()) {

			List<String> existingDisjntLst = ontoMap.get(key).getDisjointCls();

			// Now add all the disjoint class(es) of immediate parent(s)
			List<String> parent_cls_key_arr = ontoMap.get(key).getParentCls();
			for (String parent_cls_key : parent_cls_key_arr) {
				if (!(OntoConst.OntoThngCnst.equals(parent_cls_key)
						|| OntoConst.OntoNoThngCnst.equals(parent_cls_key))) {
					List<String> disjnt_cls_key_arr = ontoMap.get(parent_cls_key).getDisjointCls();
					for (String disjnt_cls_key : disjnt_cls_key_arr) {
						if (!existingDisjntLst.contains(disjnt_cls_key)) {
							existingDisjntLst.add(disjnt_cls_key);
						}
					}
				}
			}

			ontoMap.get(key).setDisjointCls(existingDisjntLst);
		}
	}

	private void getEqCls(OntoInfoModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) throws Exception {

		for (String key : ontoMap.keySet()) {
			OWLClass outerClaz = ontoFileModel.getDataFactory().getOWLClass(IRI.create(key));

			Iterator<OWLClassExpression> eqItr = EntitySearcher
					.getEquivalentClasses(outerClaz, ontoFileModel.getOntology()).iterator();
			List<String> strLst = new ArrayList<String>();

			while (eqItr.hasNext()) {
				OWLClassExpression oce = eqItr.next();
				String eqVal = oce.toString();

				if (owlUtil.isNotCls(oce.getClassExpressionType())) {
					strLst.add(owlUtil.getComplex(eqVal));
				} else {
					// <http://human.owl#NCI_C25444>
					// this is to remove < and > from the value
					eqVal = eqVal.substring(1, eqVal.length() - 1);
					if (!eqVal.equals(key)) {
						if (!(OntoConst.OntoThngCnst.equals(eqVal) || OntoConst.OntoNoThngCnst.equals(eqVal))) {
							strLst.add(eqVal);
						}
					}
				}

			}

			ontoMap.get(key).setEqCls(strLst);
		}

		// parent details is populated before
		// outside of the for loop confirms that each class has disjoint
		// classes.
		// so every parent class should have disjoint class information
		for (String key : ontoMap.keySet()) {

			List<String> existingEqLst = ontoMap.get(key).getEqCls();

			// Now add all the disjoint class(es) of immediate parent(s)
			List<String> parent_cls_key_arr = ontoMap.get(key).getParentCls();
			for (String parent_cls_key : parent_cls_key_arr) {
				if (!(OntoConst.OntoThngCnst.equals(parent_cls_key)
						|| OntoConst.OntoNoThngCnst.equals(parent_cls_key))) {
					List<String> eq_cls_key_arr = ontoMap.get(parent_cls_key).getEqCls();
					for (String eq_cls_key : eq_cls_key_arr) {
						if (!existingEqLst.contains(eq_cls_key)) {
							existingEqLst.add(eq_cls_key);
						}
					}
				}
			}
			ontoMap.get(key).setEqCls(existingEqLst);
		}

	}

	// https://tutorial-academy.com/owlapi-5-read-class-restriction-axiom-visitor/
	// https://stackoverflow.com/questions/46170981/retrieve-owl-class-restrictions-using-owl-api
	// https://owlcs.github.io/owlapi/apidocs_4/org/semanticweb/owlapi/model/ClassExpressionType.html
	// https://github.com/owlcollab/owltools/blob/master/OWLTools-Core/src/main/java/owltools/mooncat/Mooncat.java
	// https://stackoverflow.com/questions/47980787/getting-object-properties-and-classes
	// https://stackoverflow.com/questions/28968495/retrieve-owlrestrictions-using-the-owl-api
	private void getRestriction(OntoInfoModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) throws Exception {

		for (String key : ontoMap.keySet()) {
			List<String> restrictionLst = new ArrayList<String>();
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

							// Restriction with "some"
							public void visit(OWLObjectSomeValuesFrom someValuesFromAxiom) {
								getQuantifiedRestriction(someValuesFromAxiom, restrictionLst);
							}

							// Restriction with "value" ##data property
							public void visit(OWLDataHasValue hasValuesFromAxiom) {
								getDataRestriction(hasValuesFromAxiom, restrictionLst);
							}

							// Restriction with "exact"
							public void visit(OWLObjectExactCardinality exactValuesFromAxiom) {
								getCardinalityaRestriction(exactValuesFromAxiom, restrictionLst);
							}

							// Restriction with "min"
							public void visit(OWLObjectMinCardinality minValuesFromAxiom) {
								getCardinalityaRestriction(minValuesFromAxiom, restrictionLst);
							}

							// Restriction with "max"
							public void visit(OWLObjectMaxCardinality maxValuesFromAxiom) {
								getCardinalityaRestriction(maxValuesFromAxiom, restrictionLst);
							}
						});
					}
				});
			}
			ontoMap.get(key).setRestriction(restrictionLst);
		}

		// parent details is populated before
		// outside of the for loop confirms that each class has restriction
		// classes.
		// so every parent class should have restriction class information
		for (String key : ontoMap.keySet()) {

			List<String> existingResLst = ontoMap.get(key).getRestriction();

			// Now add all the restriction class(es) of immediate parent(s)
			List<String> parent_cls_key_arr = ontoMap.get(key).getParentCls();
			for (String parent_cls_key : parent_cls_key_arr) {
				if (!(OntoConst.OntoThngCnst.equals(parent_cls_key)
						|| OntoConst.OntoNoThngCnst.equals(parent_cls_key))) {
					List<String> res_cls_Lst = ontoMap.get(parent_cls_key).getRestriction();
					for (String res_cls : res_cls_Lst) {

						if (!existingResLst.contains(res_cls)) {
							existingResLst.add(res_cls);
						}
					}
				}
			}
			ontoMap.get(key).setRestriction(existingResLst);
		}
	}

	// Example
	// http://human.owl#NCI_C32546
	// ClassExpressionType: ObjectSomeValuesFrom
	// #restriction.getClassExpressionType().toString()
	// Property: <http://human.owl#UNDEFINED_part_of>
	// #restriction.getProperty().toString()
	// Object: <http://human.owl#NCI_C12393> #restriction.getFiller().toString()

	public void getQuantifiedRestriction(OWLQuantifiedObjectRestriction restriction, List<String> restrictionLst) {
		String prop = restriction.getProperty().toString();
		String obj = restriction.getFiller().toString();
		// <http://human.owl#NCI_C25444>
		// this is to remove < and > from the value
		obj = obj.substring(1, obj.length() - 1);
		String res = "(" + prop + "," + obj + ")";
		restrictionLst.add(res);
	}

	public void getDataRestriction(OWLDataHasValue restriction, List<String> restrictionLst) {
		String prop = restriction.getProperty().toString();
		String obj = restriction.getFiller().getLiteral().toString();
		// <http://human.owl#NCI_C25444>
		// this is to remove < and > from the value
		// obj = obj.substring(1, obj.length() - 1);

		String res = "(" + prop + "," + obj + ")";
		restrictionLst.add(res);
	}

	public void getCardinalityaRestriction(OWLObjectCardinalityRestriction restriction, List<String> restrictionLst) {
		String prop = restriction.getProperty().toString();
		String obj = restriction.getFiller().toString();
		// <http://human.owl#NCI_C25444>
		// this is to remove < and > from the value
		obj = obj.substring(1, obj.length() - 1);
		String res = "(" + prop + "," + obj + ")";
		restrictionLst.add(res);
	}

	private void getObjProps(OntoInfoModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) throws Exception {

		Stream<OWLObjectProperty> allObjProps = ontoFileModel.getOntology().objectPropertiesInSignature();
		allObjProps.forEach(objProp -> {

			Set<OWLAnnotation> annoLst = EntitySearcher
					.getAnnotations(objProp, ontoFileModel.getOntology(), ontoFileModel.getDataFactory().getRDFSLabel())
					.collect(Collectors.toSet());
			String key = objProp.getIRI().toString();
			String lbl = "";
			for (OWLAnnotation anno : annoLst) {
				OWLAnnotationValue val = anno.getValue();
				if (val instanceof OWLLiteral) {
					String value = ((OWLLiteral) val).getLiteral();
					lbl = lbl + " " + value;
				}
			}

			if ("".equals(lbl)) {
				lbl = key.split("#")[1];
			}

			OntoSimClsModel ontoSim = new OntoSimClsModel();
			ontoSim.setIri(key);
			ontoSim.setLbl(lbl);
			ontoSim.setEntityTyp(OntoConst.OBJ_TYP);
			ontoMap.put(key, ontoSim);

		});

	}

	private void getDataProps(OntoInfoModel ontoFileModel, Map<String, OntoSimClsModel> ontoMap) throws Exception {

		Stream<OWLDataProperty> allDataProps = ontoFileModel.getOntology().dataPropertiesInSignature();
		allDataProps.forEach(dataProp -> {

			Set<OWLAnnotation> annoLst = EntitySearcher.getAnnotations(dataProp, ontoFileModel.getOntology(),
					ontoFileModel.getDataFactory().getRDFSLabel()).collect(Collectors.toSet());
			String key = dataProp.getIRI().toString();
			String lbl = "";
			for (OWLAnnotation anno : annoLst) {
				OWLAnnotationValue val = anno.getValue();
				if (val instanceof OWLLiteral) {
					String value = ((OWLLiteral) val).getLiteral();
					lbl = lbl + " " + value;
				}
			}

			if ("".equals(lbl)) {
				lbl = key.split("#")[1];
			}

			OntoSimClsModel ontoSim = new OntoSimClsModel();
			ontoSim.setIri(key);
			ontoSim.setLbl(lbl);
			ontoSim.setEntityTyp(OntoConst.DATA_TYP);
			ontoMap.put(key, ontoSim);
		});

	}

	public File writeJson(String fl_nm, Object ontoMap) throws Exception {

		File file = new File(fl_nm);
		ObjectMapper mapper = new ObjectMapper();
		mapper.writerWithDefaultPrettyPrinter().writeValue(file, ontoMap);
		return file;
	}

}
