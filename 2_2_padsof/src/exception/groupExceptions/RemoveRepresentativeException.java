package exception.groupExceptions;

import compositePattern.Group;
import exception.GenericException;

/**
 * if you try to remove a representative from a group
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class RemoveRepresentativeException extends GenericException {
	Group group;
	public RemoveRepresentativeException( Group group) {
		super();
		this.group = group;
	}
	
	public String toString() {
		return 	group.getName() + " has as a representative \n" + group.getRepresentative();

	}
}
