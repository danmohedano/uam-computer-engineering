/**
 * Pr&aacute;ctricas de Sistemas Inform&aacute;ticos II
 * VisaCancelacionJMSBean.java
 */

package ssii2.visa;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.ejb.EJBException;
import javax.ejb.MessageDriven;
import javax.ejb.MessageDrivenContext;
import javax.ejb.ActivationConfigProperty;
import javax.jms.MessageListener;
import javax.jms.Message;
import javax.jms.TextMessage;
import javax.jms.JMSException;
import javax.annotation.Resource;
import java.util.logging.Logger;

/**
 * @author jaime
 */
@MessageDriven(mappedName = "jms/VisaPagosQueue")
public class VisaCancelacionJMSBean extends DBTester implements MessageListener {
    static final Logger logger = Logger.getLogger("VisaCancelacionJMSBean");
    @Resource
    private MessageDrivenContext mdc;

    private static final String UPDATE_CANCELA_QRY = 
                            "update pago set codrespuesta='999' " +
                            "where idautorizacion = ?";
    private static final String RECTIFICAR_SALDO_QRY = 
                            "update tarjeta " + 
                            "set saldo = saldo + importe " +
                            "from ( select numerotarjeta, importe " +
                                    "from pago " +
                                    "where idautorizacion = ?) as rectificacion " +  
                            "where rectificacion.numerotarjeta = tarjeta.numerotarjeta";



  public VisaCancelacionJMSBean() {
  }

  // TODO : Método onMessage de ejemplo
  // Modificarlo para ejecutar el UPDATE definido más arriba,
  // asignando el idAutorizacion a lo recibido por el mensaje
  // Para ello conecte a la BD, prepareStatement() y ejecute correctamente
  // la actualización
    public void onMessage(Message inMessage) {
        TextMessage msg = null;
        Connection con = null;
        PreparedStatement pstmt = null;

        try {
            if (inMessage instanceof TextMessage) {
                msg = (TextMessage) inMessage;
                logger.info("MESSAGE BEAN: Message received: " + msg.getText());
                
                if (msg.getText() == null) logger.warning("Mensaje sin texto.");
                else{
                    con = getConnection();
                    // Se cambia el codigo del pago
                    String update_codigo = UPDATE_CANCELA_QRY;
                    logger.info(update_codigo);
                    pstmt = con.prepareStatement(update_codigo);
                    pstmt.setInt(1, Integer.parseInt(msg.getText()));
                    if (!pstmt.execute() && pstmt.getUpdateCount() == 1){
                        // Rectificar el saldo del cliente
                        String rectificar = RECTIFICAR_SALDO_QRY;
                        logger.info(rectificar);
                        pstmt = con.prepareStatement(rectificar);
                        pstmt.setInt(1, Integer.parseInt(msg.getText()));
                        if (!pstmt.execute() && pstmt.getUpdateCount() == 1) logger.warning("Error rectificando saldo.");
                    }
                    else logger.warning("Error actualizando codigo.");
                }
            } else {
                logger.warning(
                        "Message of wrong type: "
                        + inMessage.getClass().getName());
            }
        } catch (SQLException sqle) {
            sqle.printStackTrace();
        } catch (JMSException e) {
            e.printStackTrace();
            mdc.setRollbackOnly();
        } catch (Throwable te) {
            te.printStackTrace();
        } finally {
            try {
                if (pstmt != null) {
                    pstmt.close(); pstmt = null;
                }
                if (con != null) {
                    closeConnection(con); con = null;
                }
            } catch (SQLException e) {
            }
        }
    }
}
