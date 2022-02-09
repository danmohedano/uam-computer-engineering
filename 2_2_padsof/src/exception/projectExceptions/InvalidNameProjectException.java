/**
 * 
 */
package exception.projectExceptions;

/**
 * invalid name on a project
 * @author danié
 *
 */
@SuppressWarnings("serial")
public class InvalidNameProjectException extends InvalidInfoProjectException {

	public InvalidNameProjectException(String invalidInfo) {
		super(invalidInfo);
	}

	public String toString() {
		return "\"" + this.invalidInfo + "\"" + " is an invalid name. Max length of 25 characters.";
	}
}
