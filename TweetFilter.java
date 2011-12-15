
import it.unipi.di.tms.config.ConfigManager;
import it.unipi.di.tms.semantic.Annotator;
import it.unipi.di.tms.semantic.RelatednessCache;
import it.unipi.di.tms.semantic.Annotation;
import it.unipi.di.tms.semantic.Similarity;
import it.unipi.di.tms.preprocessor.wiki.articles.ArticleSearcher;
import it.unipi.di.tms.preprocessor.wiki.anchors.Anchor;
import it.unipi.di.tms.preprocessor.wiki.anchors.AnchorSearcher;

import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.IOException;

public class TweetFilter {

	// Get the tweet_id and the date
	public static String head_string(String input) {
		return input.replace( get_text( input ), ""); // XXX qui era sbagliato, casino con i numeri all'inizio del testo
	}

	// Get the text
	public static String get_text(String input) {
		return input.replaceFirst("\\d+ \\d+ ", "");
	}

	public static void main(String[] args)throws Exception{
		String lang="it";
		ConfigManager.init("/home/ir2011/ir.tms.xml");  
		Annotator annotator = new Annotator(lang);
		ArticleSearcher as = new ArticleSearcher(lang);  
		RelatednessCache r = new RelatednessCache( lang );

		/*
		AnchorSearcher a_searcher = new AnchorSearcher("it");
		Anchor an=a_searcher.searchAnchor("politica"); 

		for(int wid:an.getSortedPages()){   //getSortedPage restituisce tutti gli id degli articoli linkati da quell'ancora
		      System.out.println(as.getTitleByDoc(wid));       	
		}
		*/
		
		String filename = args[0];
		String output_filename = args[0] + ".annotation";

		String str;
		String head;
		String text;
		String id, rho, annotation;
		int counter = 1;

		List<Annotation> annots;
		List<Integer> politicsAnchors = new ArrayList<Integer> ( );

		// Aggiungo manualmente i topic su cui voglio fare il confronto
		politicsAnchors.add( as.getDocId("Politica") );
		politicsAnchors.add( as.getDocId("Governo") );
		politicsAnchors.add( as.getDocId("Silvio Berlusconi") );
		politicsAnchors.add( as.getDocId("Pier Luigi Bersani") );
		politicsAnchors.add( as.getDocId("Beppe Grillo") );
		politicsAnchors.add( as.getDocId("Matteo Renzi") );
		politicsAnchors.add( as.getDocId("Gianfranco Fini") );
		politicsAnchors.add( as.getDocId("Italia dei Valori") );

		try {
			BufferedReader in = new BufferedReader(new FileReader(filename));
			PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(output_filename)));

			while ((str = in.readLine()) != null) {
				head = head_string(str);
				text = get_text(str);

				annots = annotator.annotates(text);
				float score = 0.0f;
				for(Annotation a:annots){
					if (a.getSense() != -2) { //Not disambiguated
						//id = String.valueOf(a.getSense());
						//rho = String.valueOf(a.getRho());

						for ( Integer topic : politicsAnchors ) {
							score += a.getRho() * r.rel( topic, a.getSense() );					
						}

						//annotation = as.getTitleByDoc(id);
						//head += " # " + id + " " + rho + " " + annotation;
					}
				}
				//head += score + " " + text;
				out.println(score + " " + text);
				// Counter to have a feeling of progress
				if(counter % 50000 == 0) {
					System.out.println(counter);
				}
				counter += 1;
			}

			in.close();
			out.close();

		} catch (IOException e) {
			System.out.println(e);
		}

	}

}
