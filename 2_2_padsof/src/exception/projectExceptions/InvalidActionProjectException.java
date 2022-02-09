/**
 * 
 */
package exception.projectExceptions;

/**
 * if you try an invalid action on project
 * @author danié
 *
 */
@SuppressWarnings("serial")
public class InvalidActionProjectException extends GenericProjectException {
	private String invalidAction;

	public InvalidActionProjectException(String invalidAction) {
		super();
		this.invalidAction = invalidAction;
	}
	
	public String toString() {
		return invalidAction;
	}
}
