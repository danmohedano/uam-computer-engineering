package ads.assignment3;

import java.util.*;
import java.io.*;

/**
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class ApplianceReader {

    /**
     * Method to read appliances' data from file. Doesn't allow for repeated appliances.
     * @param filename the file to read
     * @return List<Appliance> list of appliances read
     */
    public static List<Appliance> readAppliances(String filename) throws IOException
    {
        if (filename == null) return null;
        BufferedReader buffer = new BufferedReader(
                                    new InputStreamReader(
                                        new FileInputStream(filename)));

        String line;
        List <Appliance> readApps = new ArrayList<Appliance>();
        while((line = buffer.readLine()) != null)
        {
        	int n = 0;
        	List <String> data = new ArrayList<String>();
        	for (String word : line.split("="))
        	{
        		++n;
        		data.add(word);
        	}
            if (n == 5) 
            {
            	if (Television.check(data))
            	{
            		Television x = new Television(data);
                    if (readApps.contains(x) == false) readApps.add(x);
            	}
            }
            else if (n == 9)
            {
            	if (Refrigerator.check(data))
            	{
            		Refrigerator x = new Refrigerator(data);
            		if (readApps.contains(x) == false) readApps.add(x);
            	}
            }
            else if (n == 10)
            {
            	if (Washer.check(data))
            	{
            		Washer x = new Washer(data);
                    if (readApps.contains(x) == false) readApps.add(x);
            	}
            }
        }

        buffer.close();
        return readApps;
    }
}
