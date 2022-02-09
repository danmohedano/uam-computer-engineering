package exception.groupExceptions;

import compositePattern.Group;
import compositePattern.User;

/**
 * if the user already is contained in a father
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class FatherContainsUserException extends GroupContainsUserException {

	public FatherContainsUserException(User user, Group group) {
		super(user, group);
	}
	
	public String toString() {
		return super.toString() + " in supergroup";
	}
}
