/**
 * 
 */
package exception.projectExceptions;

/**
 * invalid description on a project
 * @author danié
 *
 */
@SuppressWarnings("serial")
public class InvalidDescriptionProjectException extends InvalidInfoProjectException {
	public InvalidDescriptionProjectException(String invalidInfo) {
		super(invalidInfo);
	}

	public String toString() {
		return "\"" + this.invalidInfo + "\"" + " is an invalid description. Max length of 500 characters.";
	}
}
