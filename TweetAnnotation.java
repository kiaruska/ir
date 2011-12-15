import it.unipi.di.tms.config.ConfigManager;
import it.unipi.di.tms.semantic.Annotator;
import it.unipi.di.tms.semantic.RelatednessCache;
import it.unipi.di.tms.semantic.Annotation;
import it.unipi.di.tms.semantic.Similarity;
import it.unipi.di.tms.preprocessor.wiki.articles.ArticleSearcher;

import java.util.List;

import java.io.BufferedReader;
import java.io.FileReader;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.PrintWriter;

import java.io.IOException;

public class TweetAnnotation {

    // Just remove the initial numbering to obtain the real text
    public static String head_string(String input) {
        return input.replaceFirst("\\D+.*", "");
    }

    // Just remove the initial numbering to obtain the real text
    public static String process_string(String input) {
        return input.replaceFirst("\\d+", "");
    }

	public static void main(String[] args)throws Exception{
		String lang="it";
		ConfigManager.init("/home/ir2011/ir.tms.xml");  
		// RelatednessCache r = new RelatednessCache(lang);
		Annotator annotator = new Annotator(lang);
		ArticleSearcher as = new ArticleSearcher(lang);  

        //String filename = "/l/disc3/home/ir2011/paurullan/data/TweetTwitter-20110912_160840.tweet.clean";
	String filename = args[0];
        String output_filename = args[0]+".annotation";
	//"/l/disc3/home/ir2011/paurullan/data/TweetTwitter-20110912_160840.tweet.annotation";
	// head file:
        //String filename = "/l/disc3/home/ir2011/paurullan/data/TweetTwitter-20110912_160840.tweet.head_10.clean";
        //String output_filename = "/l/disc3/home/ir2011/paurullan/data/TweetTwitter-20110912_160840.tweet.head_10.annotation";

        String str;
        String real_text;
        String annot_output;

        int counter = 0;

		List<Annotation> annots;

        try {
            BufferedReader in = new BufferedReader(new FileReader(filename));
            PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(output_filename)));
 
            while ((str = in.readLine()) != null) {
                real_text = process_string(str);
                annot_output = head_string(str);

                // annots = annotator.annotates(real_text, r);
                annots = annotator.annotates(real_text);
                for(Annotation a:annots){
                    if (a.getSense() != -2) {//Not disambiguated
                        annot_output += " # " + as.getTitleByDoc(a.getSense());
                    }
                }
                out.println(annot_output);
                // Counter to have a feeling of progress
                if(counter % 5000 == 0) {
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
