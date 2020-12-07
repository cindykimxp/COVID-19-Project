package final_project;
import java.util.Scanner;
import java.io.File;
import java.util.ArrayList;
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
			for(int f = counter; f < counter + 10; f++) {
				double min = Double.NEGATIVE_INFINITY;
				ArrayList<TFIDFword> RepTFIDFRes =  TFIDFword.TF(repDocSet.get(f), demDocSet);
				//System.out.println(RepTFIDFRes);
				TFIDFword maxWord = new TFIDFword();
				for(int i = 0; i < RepTFIDFRes.size(); i++) {
					//myWriter.write(RepTFres.get(i).getWord());
					double currentTFIDF = RepTFIDFRes.get(i).getTFIDF();
					//System.out.println(currentTFIDF);
					if(currentTFIDF > min) {
						//System.out.print(RepTFIDFRes.get(i).getWord() + ": ");
						min = currentTFIDF;
						//System.out.println(min);
						maxWord.setWord(RepTFIDFRes.get(i).getWord());
						maxWord.setTFIDF(min);
					}
					//myWriter.write(RepTFres.get(i).getTFIDF());
				}
				DemMaxRes.add(maxWord);
			}	
			
			
			for(int j = 0; j < DemMaxRes.size(); j++) {
				//System.out.print(DemMaxRes.get(j).getWord() + " ");
				myWriter.write(DemMaxRes.get(j).getWord() + " ");
				//System.out.println(DemMaxRes.get(j).getTFIDF());
				String maxTFIDF = String.valueOf(DemMaxRes.get(j).getTFIDF());
				myWriter.write(maxTFIDF);
				myWriter.write("\n");
			}
		
		demSC.close();
		//repSC.close();
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
	
	
	public static ArrayList<TFIDFword> TF(ArrayList<String> doc, ArrayList<ArrayList<String>> docSet) {
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
				IDF(docSet, word);
				//System.out.println(word.getWord());
				//System.out.println(word.getFullOcurrence());
				if(word.getFullOcurrence() != -1) {
					//System.out.println(word.getFullOcurrence());
					double TFIDF = Math.round(counter * Math.log(docSet.size() * 1.0 / word.getFullOcurrence()) * 100.0) / 100.0;
					//System.out.println(TFIDF);
					word.setTFIDF(TFIDF);
					TFwords.add(word);
				}
			}
		}
		return TFwords;
	}
	
	public static void IDF(ArrayList<ArrayList<String>> docSet, TFIDFword targetWord){
		int fullOccurrence = 0;
		for(int docCounter = 0; docCounter < docSet.size(); docCounter++) {
			ArrayList<String> eachDoc = docSet.get(docCounter);
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
	
	/**
	 * 
	 * 

		public static ArrayList<TFIDFword> TF(ArrayList<String> doc, ArrayList<TFIDFword> TFIDFwords, int totalDocs) {
		ArrayList<TFIDFword> TFwords = new ArrayList<TFIDFword>();
		ArrayList<String> searchedWords = new ArrayList<String>();
		for(int i = 0; i < doc.size(); i++) {
			if(!searchedWords.contains(doc.get(i))) {
				String targetWord = doc.get(i);
				int counter = 0;
				for(int j = 0; j < doc.size(); j++) {
					if(targetWord == doc.get(j)) {
						counter++;
					}
				}
				TFIDFword word = new TFIDFword(targetWord, counter / doc.size());
				for(int k = 0; k < TFIDFwords.size(); k++) {
					TFIDFword currentTFIDFword = TFIDFwords.get(k);
					if(currentTFIDFword.getWord().equals(targetWord)){
						int fullOccurrence = currentTFIDFword.getFullOcurrence();
						word.setFullOccurrence(fullOccurrence);
						double TFIDF = Math.round(counter * Math.log(totalDocs * 1.0 / currentTFIDFword.getFullOcurrence()) * 100.0) /100.0;
						word.setTFIDF(TFIDF);
					}
				}
				TFwords.add(word);
			}
		}
		return TFwords;
	}
	
	
	public static ArrayList<TFIDFword> IDF(ArrayList<ArrayList<String>> docSet){
		ArrayList<TFIDFword> TFIDFwords = new ArrayList<TFIDFword>();
		ArrayList<String> searchedIDFwords = new ArrayList<String>();
		for(int docCounter = 0; docCounter < docSet.size(); docCounter++) {
			ArrayList<String> eachDoc = docSet.get(docCounter);
			int eachDocSize = eachDoc.size();
			for(int wordCounter = 0; wordCounter < eachDocSize; wordCounter++) {
				String targetWord = eachDoc.get(wordCounter);
				if(!searchedIDFwords.contains(targetWord)) {
					TFIDFword newIDFword = new TFIDFword(targetWord, 0);
					newIDFword.setFullOccurrence(1);
					TFIDFwords.add(newIDFword);
					searchedIDFwords.add(targetWord);
				}
				else {
					for(int counter = 0; counter < TFIDFwords.size(); counter++) {
						TFIDFword currentIDFword = TFIDFwords.get(counter);
						if(currentIDFword.getWord().equals(targetWord)){
							currentIDFword.addOneFullOccurrence();
						}
					}
				}
			}
		}
		return TFIDFwords;
	}
	*/
}

