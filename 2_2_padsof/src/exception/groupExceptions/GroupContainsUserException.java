package exception.groupExceptions;

import compositePattern.Group;
import compositePattern.User;
import exception.GenericException;


/**
 * if the user already is contained in a if the group already contains the user
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class GroupContainsUserException extends GenericException {
	User user;
	Group group;
	public GroupContainsUserException(User name, Group group) {
		super();
		this.user = name;
		this.group = group;
	}
	
	public String toString() {
		return 	group.getName() + " already contains " + user.getName();

	}
}
