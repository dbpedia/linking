package com.ontosim.adapter;

import java.io.File;
import java.nio.ByteBuffer;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.apache.commons.io.FileUtils;
import org.hobbit.core.components.AbstractSystemAdapter;
import org.hobbit.core.rabbit.RabbitMQUtils;
import org.hobbit.core.rabbit.SimpleFileReceiver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.ontosim.cnst.OntoConst;
import com.ontosim.model.OntoDbModel;

public class OntoConnAdapter extends AbstractSystemAdapter {
	
	private static final Logger LOGGER = LoggerFactory.getLogger(OntoConnAdapter.class);

	private String format;

	private String sourceName;
	private String targetName;

	private String sourcePath;
	private String targetPath;

	private String results_directory = "./ontofiles/oaei/";
	private String resultsPath = System.getProperty("user.dir") + File.separator + "ontofiles" + File.separator
			+ "oaei";

	// output file name given to the output manager, which add an additional
	// ".rdf" to the file
	private String resultsFile = resultsPath + File.separator + "ontoconn-alignment";

	private ExecutorService executor;
	private Map<String, FileReceiverCallableState> receivers = Collections
			.synchronizedMap(new HashMap<String, FileReceiverCallableState>());

	private String queueName;

	@Override
	public void init() throws Exception {
		LOGGER.info("init method START");
		super.init();
		executor = Executors.newCachedThreadPool();
		LOGGER.info("init method END");
	}

	public void receiveGeneratedData(byte[] data) {
		LOGGER.info("receiveGeneratedData method START");
		
		try {
			
			ByteBuffer dataBuffer = ByteBuffer.wrap(data);
			String format = RabbitMQUtils.readString(dataBuffer);

			while (dataBuffer.hasRemaining()) {
				queueName = RabbitMQUtils.readString(dataBuffer);

				SimpleFileReceiver receiver = SimpleFileReceiver.create(this.incomingDataQueueFactory, queueName);
				FileReceiverCallable callable = new FileReceiverCallable(receiver, results_directory);

				// Start a parallel thread that receives the data for us
				receivers.put(queueName, new FileReceiverCallableState(executor.submit(callable), callable));
			}

		}

		catch (Exception ex) {
			LOGGER.error("Exception occur:- ", ex);
		}
		
		LOGGER.info("receiveGeneratedData method END");
	}

	/**
	 * This method receives the task: source and target datasets
	 */
	public void receiveGeneratedTask(String taskId, byte[] data) {
		LOGGER.info("receiveGeneratedTask method START");
		
		Set<String> allowed_instance_types = new HashSet<String>();

		ByteBuffer taskBuffer = ByteBuffer.wrap(data);
		// read the buffer in order (8 elements)
		// 1. Format
		format = RabbitMQUtils.readString(taskBuffer);
		LOGGER.info("format " +format);
		// 2. Source file name
		sourceName = RabbitMQUtils.readString(taskBuffer);
		LOGGER.info("sourceName " +sourceName);
		// 3. Target file name
		targetName = RabbitMQUtils.readString(taskBuffer);
		LOGGER.info("targetName " +targetName);
		// 4. If class matching is required
		boolean isMatchingClassesRequired = Boolean.valueOf(RabbitMQUtils.readString(taskBuffer));
		LOGGER.info("isMatchingClassesRequired " +isMatchingClassesRequired);
		// 5. If data property matching is required
		boolean isMatchingDataPropertiesRequired = Boolean.valueOf(RabbitMQUtils.readString(taskBuffer));
		LOGGER.info("isMatchingDataPropertiesRequired " +isMatchingDataPropertiesRequired);
		// 6. If object property matching is required
		boolean isMatchingObjectPropertiesRequired = Boolean.valueOf(RabbitMQUtils.readString(taskBuffer));
		LOGGER.info("isMatchingObjectPropertiesRequired " +isMatchingObjectPropertiesRequired);
		// 7. If instance matching is required
		boolean isMatchingInstancesRequired = Boolean.valueOf(RabbitMQUtils.readString(taskBuffer));
		LOGGER.info("isMatchingInstancesRequired " +isMatchingInstancesRequired);
		// 8. Queue name (task name and id to receive the files)
		// We should have defined above a Thread to receive the files in that
		// queue, otherwise the task will not be processed (see below)
		String queueName = RabbitMQUtils.readString(taskBuffer);
		LOGGER.info("queueName " +queueName);

		// 9+ Allowed instance types (i.e., class URIs)
		if (isMatchingInstancesRequired) {
			while (taskBuffer.hasRemaining()) {
				// Update allowed_instance_types
				allowed_instance_types.add(RabbitMQUtils.readString(taskBuffer));
			}
		}

		try {

			if (receivers.containsKey(queueName)) {
				FileReceiverCallableState status = receivers.get(queueName);
				status.callable.terminateReceiver();
				String files[] = status.result.get(); // to be stored in results_directory

			} else {
				LOGGER.info("The given queue name does not exist: " + queueName);

			}

//			File file_source = new File(resultsPath + File.separator + sourceName);
//			File file_target = new File(resultsPath + File.separator + targetName);
//
//			sourcePath = getURIPath(file_source.getAbsolutePath());
//			targetPath = getURIPath(file_target.getAbsolutePath());
			
			sourcePath = resultsPath + File.separator + sourceName;
			targetPath = resultsPath + File.separator + targetName;

			String resultsFileTask = resultsFile + "-" + queueName + ".rdf";// taskId
			
			ontoConnOAEIController(sourcePath, targetPath, resultsFileTask);

			byte[][] resultsArray = new byte[1][];
			resultsArray[0] = FileUtils.readFileToByteArray(new File(resultsFileTask));
			byte[] results = RabbitMQUtils.writeByteArrays(resultsArray);

			sendResultToEvalStorage(taskId, results);

		} catch (Exception ex) {
			LOGGER.error("Exception occur:- ", ex);
		}

		LOGGER.info("receiveGeneratedTask method END");
	}

	public void ontoConnOAEIController(String source, String target, String resultsFileTask) throws Exception {
		LOGGER.info("ontoConnOAEIController method START");
		LOGGER.info("source " +source);
		LOGGER.info("target " +target);
		LOGGER.info("resultsFileTask " +resultsFileTask);
		try {
			OntoConnController ontoConnController = new OntoConnController();

			//Make it finalize before submit
			OntoDbModel ontoDbModel = new OntoDbModel();
			ontoDbModel.setDb_nm(OntoConst.DS_1);
			ontoDbModel.setVec_dim(OntoConst.vec_dim);
			ontoDbModel.setWord_wt_ds(OntoConst.word_wt_ds);
			ontoDbModel.setMeta_wt_ds(OntoConst.meta_wt_ds);
			ontoDbModel.setOp_k(OntoConst.op_k);
			ontoDbModel.setThreshold_ds(OntoConst.threshold_ds);
			
			ontoConnController.ontoConnController(source, target, resultsFileTask, ontoDbModel);
		} catch (Exception e) {
			LOGGER.error("Exception occur", e);
			throw e;
		}

		LOGGER.info("ontoConnOAEIController method END");
	}

	private String getURIPath(String file_path) {

		LOGGER.info("getURIPath method START");
		String fl_path = "";
		if (file_path.startsWith("file:") || file_path.startsWith("http://")) {
			fl_path = file_path;
		}

		if (file_path.startsWith("/")) {
			fl_path = "file:" + file_path; // linux
		}
		fl_path = "file:/" + file_path; // windows

		LOGGER.info("getURIPath method END");
		return fl_path;
	}

}
