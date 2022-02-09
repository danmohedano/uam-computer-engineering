/**
 * 
 */
package exception.projectExceptions;

import project.Project;

/**
 * project exists already
 * @author danié
 *
 */
@SuppressWarnings("serial")
public class PreExistingProjectException extends GenericProjectException {
	private Project p;
	public PreExistingProjectException(Project p) {
		super();
		this.p = p;
	}
	
	public String toString() {
		return "A project with name \"" + p.getName() + "\" already exists.";
	}
}
