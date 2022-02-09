package exception.groupExceptions;

import compositePattern.Group;
import exception.GenericException;
import project.Project;

/**
 * if the project is already added to the group
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
@SuppressWarnings("serial")
public class ProjectAlreadyAddedException extends GenericException {
	Project project;
	Group group;
	public ProjectAlreadyAddedException(Project project, Group group) {
		super();
		this.project = project;
		this.group = group;
	}
	
	public String toString() {
		return project.getName() + " is already added to " + group.getName();

	}
}
