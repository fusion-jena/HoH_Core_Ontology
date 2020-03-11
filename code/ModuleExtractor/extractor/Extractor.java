package extractor;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Optional;
import java.util.Set;
import java.util.zip.GZIPInputStream;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.io.RDFOntologyFormat;
import org.semanticweb.owlapi.io.RDFXMLOntologyFormat;
import org.semanticweb.owlapi.io.StreamDocumentSource;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.MissingImportHandlingStrategy;
import org.semanticweb.owlapi.model.OWLEntity;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyID;
import org.semanticweb.owlapi.model.OWLOntologyLoaderConfiguration;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;

import uk.ac.manchester.cs.owlapi.modularity.ModuleType;



public class Extractor {

	public static void main(String[] args) throws OWLOntologyCreationException, IOException {
		// TODO Auto-generated method stub
		 double start=System.currentTimeMillis();
	     String fp1 = "C:\\Users\\RS\\eclipse-workspace\\moduleExtractor\\src\\ressource\\Thesaurus.owl";
	     ArrayList<String> terms=new ArrayList<String>();
	     terms.add("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C25688");
		 int m=0;
	     OWLOntology mod=run(fp1,terms,m);
	     String loc="C:\\Users\\RS\\eclipse-workspace\\moduleExtractor\\src\\result\\results_ncit_status.owl";
	     saveOntology(mod,loc);
	     double end=System.currentTimeMillis();
	     System.out.println(mod.getAxiomCount()+"\t The optimal num. of partition time---->"+(end-start)*.001+"\t sec \t");

	}
	
	private static void saveOntology(OWLOntology owlN, String loc)
	 {
	     OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
	     RDFXMLOntologyFormat format= new RDFXMLOntologyFormat();
	     //OWLDocumentFormat format=new RDFXMLDocumentFormat();
	     File file=new File(loc);
	     try {
	        manager.saveOntology(owlN, format, IRI.create(file.toURI()));
	    } catch (OWLOntologyStorageException e) {
	        e.printStackTrace();
	    }
	   /*  OntDocumentManager mgr = new OntDocumentManager();
	     mgr.setProcessImports(true);
	     OntModelSpec spec = new OntModelSpec(OntModelSpec.OWL_MEM);
	     Reasoner reasoner = ReasonerRegistry.getOWLReasoner();
	     spec.setDocumentManager(mgr);
	     OntModel model = ModelFactory.createOntologyModel(spec, null);
	     try{
	     model.read("file:"+loc);}
	     catch(RiotException e){}
	      model.setStrictMode(false);
	     models.add(model);*/
	 }
	
	public static OWLOntology run(String Ontname, ArrayList<String> terms, int m) 
	{
		InputStream in=null;
    	InputStream fileStream=null;
    	if(Ontname.endsWith(".owl")||Ontname.endsWith(".rdf"))
			try {
				in = new FileInputStream(Ontname);
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		else if(Ontname.endsWith(".obo"))
			try {
				in = new FileInputStream(Ontname);
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		else if(Ontname.endsWith(".gz"))
    		{
    			try {
					fileStream = new FileInputStream(new File(Ontname));
				} catch (FileNotFoundException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
    			try {
					in= new GZIPInputStream(fileStream);
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
    		}
    	
    	OWLOntologyLoaderConfiguration config = new OWLOntologyLoaderConfiguration();
        config = config.setMissingImportHandlingStrategy(MissingImportHandlingStrategy.SILENT);
        StreamDocumentSource documentSource = new StreamDocumentSource(in);
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
    	 OWLOntology owl=null;
		 try {
			owl = manager.loadOntologyFromOntologyDocument(documentSource,config);
		} catch (OWLOntologyCreationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		 Set<OWLEntity> signature = null;
		 signature = ModuleExtractor.getSignature(owl, terms);
		 OWLOntology mod = null;
		 IRI id=owl.getOntologyID().getOntologyIRI();
		 //System.out.println(id+"\t"+owl.getOntologyID().getDefaultDocumentIRI());
		 String moduleName;
		 if(id!=null)
		  moduleName = id.toString();
		 else
			 moduleName=in.toString();
		 ModuleType modType = null;
			
			switch(m) {
			case 0: modType = ModuleType.STAR; break;
			case 1: modType = ModuleType.BOT; break;
			case 2: modType = ModuleType.TOP; break;
			}
			if(moduleName.contains(".owl"))
				moduleName = moduleName.substring(0, moduleName.indexOf(".owl")) + "_module" + 1 + ".owl";
			else if(moduleName.contains(".rdf"))
				moduleName = moduleName.substring(0, moduleName.indexOf(".rdf")) + "_module" + 1 + ".rdf";
			else
				moduleName = moduleName + "module"  + 1;
		 try {
				mod = ModuleExtractor.extractModule(signature, owl, moduleName,  modType);
			} catch (OWLOntologyCreationException e) {
				e.printStackTrace();
			}
		 return mod;
	}

}
