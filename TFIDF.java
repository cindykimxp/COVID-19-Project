package final_project;
import java.util.Scanner;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.io.FileWriter;



public class TFIDF{
	public static void main(String[] args) throws Exception{
		ArrayList<ArrayList<String>> demDocSet = new ArrayList<ArrayList<String>>();
		ArrayList<ArrayList<String>> repDocSet = new ArrayList<ArrayList<String>>();
		File demFile = new File("/users/jingyi/desktop/NLP_Final_Project/dem_dev_lemma.txt");
		File repFile = new File("/users/jingyi/desktop/NLP_Final_Project/rep_dev_lemma.txt");
		Scanner demSC = new Scanner(demFile);
		Scanner repSC = new Scanner(repFile);
		getDocSet(demDocSet, demSC);
		getDocSet(repDocSet, repSC);
		//System.out.println(Math.round(1.2345238432342));
		
		ArrayList<TFIDFword> DemMaxRes = new ArrayList<TFIDFword>();

				
			FileWriter myWriter = new FileWriter("/users/jingyi/desktop/NLP_Final_Project/dem_dev_res.txt");
			int counter  = 0;
			boolean lock = true;
			System.out.println(demDocSet.size());
			System.out.println(repDocSet.size());
			while(lock) {
				for(int f = counter; f < counter + 10; f++) {
					System.out.println(f);
					if((f + 10) >= repDocSet.size() || (f + 10) >= demDocSet.size()) {
						
						mainCalculate(demDocSet, repDocSet, DemMaxRes, f, demDocSet.size());
						lock = false;
						break;
					}
					else {
						mainCalculate(demDocSet, repDocSet, DemMaxRes, f, f + 10);
					}
				}
				counter += 10;
			}
			
			for(int j = 0; j < DemMaxRes.size(); j++) {
				System.out.println(DemMaxRes.get(j).getWord() + " ");
				myWriter.write(DemMaxRes.get(j).getWord() + " ");
				String maxTFIDF = String.valueOf(DemMaxRes.get(j).getTFIDF());
				System.out.println(maxTFIDF);
				myWriter.write(maxTFIDF);
				myWriter.write("\n");
			}
		
		demSC.close();
		//repSC.close();
	}
	
	public static void mainCalculate(ArrayList<ArrayList<String>> comparedDataSet, ArrayList<ArrayList<String>> comparingDataSet,  ArrayList<TFIDFword> DemMaxRes, int currentIndex, int endingIndex) {
		double min = Double.NEGATIVE_INFINITY;
		ArrayList<ArrayList<String>> copyOfDataSet = comparedDataSet;
		ArrayList<TFIDFword> comparingTFIDFRes =  TFIDFword.TF(comparingDataSet.get(currentIndex), copyOfDataSet.subList(currentIndex, endingIndex));
		TFIDFword maxWord = new TFIDFword();
		for(int i = 0; i < comparingTFIDFRes.size(); i++) {
			double currentTFIDF = comparingTFIDFRes.get(i).getTFIDF();
			//System.out.println(currentTFIDF);
			if(currentTFIDF > min) {
				min = currentTFIDF;
				maxWord.setWord(comparingTFIDFRes.get(i).getWord());
				maxWord.setTFIDF(min);
				//System.out.println(maxWord);
			}
		}
		DemMaxRes.add(maxWord);
	}

	
	public static ArrayList<ArrayList<String>> getDocSet(ArrayList<ArrayList<String>> docSet, Scanner sc) {
		while(sc.hasNextLine()) {
			String line = sc.nextLine();
			//System.out.println(line);
			if(line.contains("+00:00")) {
				sc.nextLine();
				//System.out.println(line);
				ArrayList<String> doc = new ArrayList<String>();
				while(sc.hasNextLine()) {
					String innerLine = sc.nextLine(); 
					//System.out.println(innerLine);
					if(innerLine.length() == 0) {
						break;
					}
					else {
						String word = "";
						for(int j = 0; j < innerLine.length(); j++) {
							if(!Character.isLetter(innerLine.charAt(j))) {
								word = innerLine.substring(0, j);
								//System.out.println(word);
							}
						}
						doc.add(word);
					}
				}
				docSet.add(doc);
			}
		}
		//System.out.println(docSet);
		return docSet;
	}
	
}	

class TFIDFword{
		private String word;
		private int occurrence;
		private int fullOccurrence;
		private double TFIDF;
		
		TFIDFword(){
			
		}
		
		TFIDFword(String word, int occurence){
			this.word = word;
			this.occurrence = occurence;
		}
		
		void setWord(String word){
			this.word = word;
		}
		
		String getWord() {
			return this.word;
		}
		
		void setOccurrence(int occurrence) {
			this.occurrence = occurrence;
		}
		
		int getOcurrence() {
			return this.occurrence;
		}
		
		void addOneOccurrence() {
			this.occurrence += 1;
		}
		
		void setFullOccurrence(int fullOccurrence) {
			this.fullOccurrence = fullOccurrence;
		}
		
		void addOneFullOccurrence() {
			this.fullOccurrence += 1;
		}
		
		int getFullOcurrence() {
			return this.fullOccurrence;
		}
		
		void setTFIDF(double TFIDF) {
			this.TFIDF = TFIDF;
		}
		
		double getTFIDF() {
			return this.TFIDF;
		}
	
	
	public static ArrayList<TFIDFword> TF(ArrayList<String> doc, List<ArrayList<String>> list) {
		ArrayList<TFIDFword> TFwords = new ArrayList<TFIDFword>();
		ArrayList<String> searchedWords = new ArrayList<String>();
		for(int i = 0; i < doc.size(); i++) {
			String targetWord = doc.get(i);
			if(!searchedWords.contains(targetWord)) {
				int counter = 0;
				for(int j = 0; j < doc.size(); j++) {
					if(targetWord == doc.get(j)) {
						counter++;
					}
				}
				TFIDFword word = new TFIDFword(targetWord, counter / doc.size());
				IDF(list, word);
				if(word.getFullOcurrence() != -1) {
					double TFIDF = Math.round(counter * Math.log(list.size() * 1.0 / word.getFullOcurrence()) * 100.0) / 100.0;
					//System.out.println(TFIDF);
					word.setTFIDF(TFIDF);
					TFwords.add(word);
				}
			}
		}
		return TFwords;
	}
	
	public static void IDF(List<ArrayList<String>> list, TFIDFword targetWord){
		int fullOccurrence = 0;
		for(int docCounter = 0; docCounter < list.size(); docCounter++) {
			ArrayList<String> eachDoc = list.get(docCounter);
			int eachDocSize = eachDoc.size();
			for(int wordCounter = 0; wordCounter < eachDocSize; wordCounter++) {
				String currentWord = eachDoc.get(wordCounter);
				if(currentWord.toLowerCase().equals(targetWord.getWord().toLowerCase())) {
					fullOccurrence += 1; 
					break;
				}
			}
		}
		if(fullOccurrence == 0) {
			targetWord.setFullOccurrence(-1);
		}	
		else {
		targetWord.setFullOccurrence(fullOccurrence);
		}
	}

}

