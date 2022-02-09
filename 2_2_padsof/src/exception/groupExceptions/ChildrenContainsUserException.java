package exception.groupExceptions;

import compositePattern.Group;
import compositePattern.User;


/**
 * if the user already is contained in a child
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class ChildrenContainsUserException extends GroupContainsUserException {

	public ChildrenContainsUserException(User user, Group group) {
		super(user, group);
	}
	
	public String toString() {
		return super.toString() + " in subgroups";
	}
}
