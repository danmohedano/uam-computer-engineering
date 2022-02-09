package exception.appExceptions;

import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import exception.GenericException;

/**
 * if the application is already logged in
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class AlreadyLogInException extends GenericException {
	RegisteredCitizen user;
	Group group;
	public AlreadyLogInException(RegisteredCitizen person) {
		super();
		this.user = person;
	}
	
	public String toString() {
		return user.getName() + " is already logged in.";

	}
}
