package com.ontosim.model;

public class OntoServiceModel {

	OntoFileModel src_in_data;
	OntoFileModel trgt_in_data;
	OntoFileModel final_op_data;
	OntoFileModel aux_op_data;
	OntoFileMsg msg;
	
	public OntoFileModel getSrc_in_data() {
		return src_in_data;
	}
	public void setSrc_in_data(OntoFileModel src_in_data) {
		this.src_in_data = src_in_data;
	}
	public OntoFileModel getTrgt_in_data() {
		return trgt_in_data;
	}
	public void setTrgt_in_data(OntoFileModel trgt_in_data) {
		this.trgt_in_data = trgt_in_data;
	}
	public OntoFileModel getFinal_op_data() {
		return final_op_data;
	}
	public void setFinal_op_data(OntoFileModel final_op_data) {
		this.final_op_data = final_op_data;
	}
	public OntoFileModel getAux_op_data() {
		return aux_op_data;
	}
	public void setAux_op_data(OntoFileModel aux_op_data) {
		this.aux_op_data = aux_op_data;
	}
	public OntoFileMsg getMsg() {
		return msg;
	}
	public void setMsg(OntoFileMsg msg) {
		this.msg = msg;
	}

}
