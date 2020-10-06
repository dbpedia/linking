package com.ontosim.model;

public class OntoDbModel {

	String db_nm;
	int vec_dim;
	int op_k;
	double word_wt_ds;
	double meta_wt_ds;
	double threshold_ds;

	public String getDb_nm() {
		return db_nm;
	}

	public void setDb_nm(String db_nm) {
		this.db_nm = db_nm;
	}

	public int getVec_dim() {
		return vec_dim;
	}

	public void setVec_dim(int vec_dim) {
		this.vec_dim = vec_dim;
	}

	public int getOp_k() {
		return op_k;
	}

	public void setOp_k(int op_k) {
		this.op_k = op_k;
	}

	public double getWord_wt_ds() {
		return word_wt_ds;
	}

	public void setWord_wt_ds(double word_wt_ds) {
		this.word_wt_ds = word_wt_ds;
	}

	public double getMeta_wt_ds() {
		return meta_wt_ds;
	}

	public void setMeta_wt_ds(double meta_wt_ds) {
		this.meta_wt_ds = meta_wt_ds;
	}

	public double getThreshold_ds() {
		return threshold_ds;
	}

	public void setThreshold_ds(double threshold_ds) {
		this.threshold_ds = threshold_ds;
	}
	
	
}
