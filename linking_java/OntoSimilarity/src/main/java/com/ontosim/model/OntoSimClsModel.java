package com.ontosim.model;

import java.util.List;

public class OntoSimClsModel {
	String lbl;
	String altLbl;
	String iri;
	String vector;
	String entityTyp;
	List<String> parentCls;
	List<String> childCls;
	List<String> eqCls;
	List<String> disjointCls;
	List<String> restriction;
	
	
	public String getLbl() {
		return lbl;
	}
	public void setLbl(String lbl) {
		this.lbl = lbl;
	}
	public String getAltLbl() {
		return altLbl;
	}
	public void setAltLbl(String altLbl) {
		this.altLbl = altLbl;
	}
	public String getIri() {
		return iri;
	}
	public void setIri(String iri) {
		this.iri = iri;
	}
	public List<String> getEqCls() {
		return eqCls;
	}
	public void setEqCls(List<String> eqCls) {
		this.eqCls = eqCls;
	}
	public List<String> getDisjointCls() {
		return disjointCls;
	}
	public void setDisjointCls(List<String> disjointCls) {
		this.disjointCls = disjointCls;
	}
	public List<String> getRestriction() {
		return restriction;
	}
	public void setRestriction(List<String> restriction) {
		this.restriction = restriction;
	}
	public String getVector() {
		return vector;
	}
	public void setVector(String vector) {
		this.vector = vector;
	}
	public List<String> getParentCls() {
		return parentCls;
	}
	public void setParentCls(List<String> parentCls) {
		this.parentCls = parentCls;
	}
	public List<String> getChildCls() {
		return childCls;
	}
	public void setChildCls(List<String> childCls) {
		this.childCls = childCls;
	}
	public String getEntityTyp() {
		return entityTyp;
	}
	public void setEntityTyp(String entityTyp) {
		this.entityTyp = entityTyp;
	}
}
