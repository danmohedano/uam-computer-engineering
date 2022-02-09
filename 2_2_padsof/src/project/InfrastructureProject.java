/**
 * 
 */
package project;

import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import javax.imageio.ImageIO;

import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import exception.projectExceptions.InvalidActionProjectException;
import exception.projectExceptions.InvalidInfoProjectException;
import exception.projectExceptions.PreExistingProjectException;

/**
 * Project Class
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
public class InfrastructureProject extends Project {
	private static final long serialVersionUID = 1L;
	private String filename; //Name of the file for the graphicalScheme
	private List<String> districtsAffected = new ArrayList<>();
	private String generatedFilename;
	public static List<String> districts; 
	private static String fileNameDistricts = "src/project/districts.txt";
	
	public InfrastructureProject(String name, String description, double money, RegisteredCitizen creator, String filename, List<String> districtsAffected) throws InvalidInfoProjectException, PreExistingProjectException, InvalidActionProjectException, Exception
	{
		super(name, description, money, creator);
		this.filename = filename;
		if (districts == null) readDistricts();
		if (districtsAffected != null && districts != null) {
			for(String x : districtsAffected) {
				if (districts.contains(x)) this.districtsAffected.add(x);
			}
		}
		this.saveImage();
	}
	
	public InfrastructureProject(String name, String description, double money, RegisteredCitizen creator, Group group, String filename, List<String> districtsAffected) throws InvalidInfoProjectException, PreExistingProjectException, Exception{
		super(name, description, money, creator, group);
		this.filename = filename;
		if (districts == null) readDistricts();
		if (districtsAffected != null && districts != null) {
			for(String x : districtsAffected) {
				if (districts.contains(x)) this.districtsAffected.add(x);
			}
		}
		this.saveImage();
	}
	
	public void saveImage() throws IOException {
		BufferedImage myPicture = ImageIO.read(new File(this.filename));
		Random random = new Random();
		//Generate a random name for the auxiliary file
		String s = "files/projectSchemes/";
		s += random.ints(97, 123).limit(15).collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append).toString();		
		s += ".jpg";
		this.generatedFilename = s;
		ImageIO.write(myPicture, "jpg", new File(s));
	}
	
	
	/**
	 * Method to load the list of districts from a text file.
	 * @throws IOException if when reading districts there is an error
	 */
	public static void readDistricts() throws IOException
	{
		BufferedReader buffer = new BufferedReader(
									new InputStreamReader(
										new FileInputStream(InfrastructureProject.fileNameDistricts)));
		String line;
		InfrastructureProject.districts = new ArrayList<>();
		
		while ((line = buffer.readLine()) != null)
		{
			InfrastructureProject.districts.add(line);
		}
		
		buffer.close();
	}
	
	/**
	 * @return the filename
	 */
	public String getFilename() {
		return filename;
	}

	/**
	 * @param filename the filename to set
	 */
	public void setFilename(String filename) {
		this.filename = filename;
	}

	@Override
	public String getExtraData() {
		String extraData=this.filename;
		for (String x : this.districtsAffected) {
			extraData += ", " + x;
		}
		return extraData;
	}

	@Override
	public ProjectKind getProjectKind() {
		return ProjectKind.Infrastructure;
	}
	
	public String toString() {
		return "(IF) " + super.toString();
	}

	/**
	 * @return the districtsAffected
	 */
	public List<String> getDistrictsAffected() {
		return districtsAffected;
	}

	/**
	 * @param districtsAffected the districtsAffected to set
	 */
	public void setDistrictsAffected(List<String> districtsAffected) {
		this.districtsAffected = districtsAffected;
	}

	/**
	 * @return the generatedFilename
	 */
	public String getGeneratedFilename() {
		return generatedFilename;
	}

	/**
	 * @param generatedFilename the generatedFilename to set
	 */
	public void setGeneratedFilename(String generatedFilename) {
		this.generatedFilename = generatedFilename;
	}
	
}
