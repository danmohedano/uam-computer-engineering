package exception.groupExceptions;

import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import exception.GenericException;

/**
 * if the user if is not contained in the group
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class MemberNotContainedException extends GenericException {
	RegisteredCitizen user;
	Group group;
	public MemberNotContainedException(RegisteredCitizen person, Group group) {
		super();
		this.user = person;
		this.group = group;
	}
	
	public String toString() {
		return user.getName() + " is not contained in " + group.getName();

	}
}
