/**
 * 
 */
package exception.projectExceptions;

/**
 * invalid threshold on an application
 * @author dani�
 *
 */
@SuppressWarnings("serial")
public class InvalidThresholdProjectException extends InvalidInfoProjectException {
	public InvalidThresholdProjectException(int invalidInfo) {
		super(Integer.toString(invalidInfo));
	}

	public String toString() {
		return "\"" + this.invalidInfo + "\"" + " is an invalid threshold. Must be positive.";
	}
}
