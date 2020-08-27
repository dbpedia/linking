package com.ontosim.util;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.ontosim.cnst.OntoConst;
import com.ontosim.exception.OntoException;

public class OntoCallReqUtil {

	private static final Logger logger = LoggerFactory.getLogger(OntoCallReqUtil.class);
	
	public String ontoPOSTRequest(String url, String jsonIp) throws Exception{
		
		logger.info("URL:- "+url);
		logger.info("POSTRequest 1");
		URL obj = new URL(url);
		logger.info("POSTRequest 2");
		HttpURLConnection postConnection = (HttpURLConnection) obj.openConnection();
	    postConnection.setRequestMethod("POST");
	    postConnection.setRequestProperty("Content-Type", "application/json; utf-8");
	    postConnection.setRequestProperty("Accept", "application/json");

	    postConnection.setDoOutput(true);
	    logger.info("POSTRequest 3");

	    OutputStream os = postConnection.getOutputStream(); 

	    os.write(jsonIp.getBytes("utf-8"));
	    os.flush();
	    os.close();

	    int responseCode = postConnection.getResponseCode();

	    logger.info("POST Response Code :  " + responseCode);
	    logger.info("POST Response Message : " + postConnection.getResponseMessage());
	    
	    if (responseCode == HttpURLConnection.HTTP_OK) { //success
	        BufferedReader in = new BufferedReader(new InputStreamReader(
	            postConnection.getInputStream(), "utf-8"));
	        String inputLine;
	        StringBuffer response = new StringBuffer();
	        while ((inputLine = in .readLine()) != null) {
	            response.append(inputLine);
	        } in .close();
	        logger.info("ontoPOSTRequest 4");
		
	        return response.toString();
	    } else {
	    	logger.info("ontoPOSTRequest 5");
	    	throw new OntoException(OntoConst.ERR_MSG_5);
	    }    
	    
	}
}
