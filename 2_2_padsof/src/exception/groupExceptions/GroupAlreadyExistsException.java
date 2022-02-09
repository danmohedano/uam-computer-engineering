package exception.groupExceptions;

import compositePattern.Group;

/**
 * group already exists exception
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class GroupAlreadyExistsException extends Exception {
	Group group;

	public GroupAlreadyExistsException(Group group) {
		this.group = group;
	}
	@Override
	public String toString() {
		return "Group already exists: " + this.group;
	}

}
