package application;

import gui.window.Window;
import persistence.Persistence;



/**
 * The demostration of the project
 * @author Silvia Sopena silvia.sopenna@estudiante.uam.es
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
public class Main 
{
	public static void main (String[] args) throws Exception 
	{
		Persistence.readAll();

		new Window();
		/*Persitence.saveAll(); moved elsewhere*/
	}
}
