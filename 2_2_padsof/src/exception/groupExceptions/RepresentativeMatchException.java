package exception.groupExceptions;

import compositePattern.RegisteredCitizen;
import exception.GenericException;

/**
 * if the representatives dont match
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class RepresentativeMatchException extends GenericException {

	public RepresentativeMatchException(RegisteredCitizen first, RegisteredCitizen second, String name1, String name2) {
		super("Representatives "+ first + " and " + second + " don't match in " + name1 + " and " + name2);
	}
}
