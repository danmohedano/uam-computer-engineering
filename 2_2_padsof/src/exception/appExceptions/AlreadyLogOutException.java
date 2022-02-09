package exception.appExceptions;

import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import exception.GenericException;

/**
 * if the application is already logged out
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class AlreadyLogOutException extends GenericException {
	RegisteredCitizen user;
	Group group;
	public AlreadyLogOutException() {
		super();
	}
	
	public String toString() {
		return "Application is already logged out";

	}
}
