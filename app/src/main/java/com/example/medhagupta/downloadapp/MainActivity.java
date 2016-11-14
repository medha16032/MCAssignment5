package com.example.medhagupta.downloadapp;



import java.io.IOException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.app.ProgressDialog;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {

    // URL Address
    String url = "http://www.iiitd.ac.in/about";
    ProgressDialog mProgressDialog;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Locate the Buttons in activity_main.xml
        Button titlebutton = (Button) findViewById(R.id.titlebutton);
        Button descbutton = (Button) findViewById(R.id.contentbutton);


        // Capture button click
        titlebutton.setOnClickListener(new OnClickListener() {
            public void onClick(View arg0) {
                // Execute Title AsyncTask
                new Title().execute();
            }
        });

        // Capture button click
        descbutton.setOnClickListener(new OnClickListener() {
            public void onClick(View arg0) {
                // Execute Description AsyncTask
                new Content().execute();
            }
        });



    }

    // Title AsyncTask
    private class Title extends AsyncTask<Void, Void, Void> {
        String title="";

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            mProgressDialog = new ProgressDialog(MainActivity.this);
            mProgressDialog.setTitle("Fetching title");
            mProgressDialog.setMessage("Loading...");
            mProgressDialog.setIndeterminate(false);
            mProgressDialog.show();
        }



        @Override
        protected Void doInBackground(Void... params) {
            try {
                // Connect to the web site
                Document document = Jsoup.connect(url).get();
                // Get the html document title
                title = document.title();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            if (title.equals("")) {

                Toast.makeText(getApplicationContext(), "Unable to access internet!!", Toast.LENGTH_SHORT).show();
            } else {
                // Set title into TextView
                TextView txttitle = (TextView) findViewById(R.id.titletxt);
                txttitle.setText(title);

            }
            mProgressDialog.dismiss();
        }
    }

    // Description AsyncTask
    private class Content extends AsyncTask<Void, Void, Void> {
        String desc;
        Document document;

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            mProgressDialog = new ProgressDialog(MainActivity.this);
            mProgressDialog.setTitle("Fetching content");
            mProgressDialog.setMessage("Loading...");
            mProgressDialog.setIndeterminate(false);
            mProgressDialog.show();
        }

        @Override
        protected Void doInBackground(Void... params) {
            try {
                // Connect to the web site
                document = Jsoup.connect(url).get();
                // Using Elements to get the Meta data
                Elements description = document
                        .select("meta[name=description]");
                // Locate the content attribute
                desc = description.attr("content");
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(Void result) {

            if (document == null) {

                Toast.makeText(getApplicationContext(), "Unable to access internet!!", Toast.LENGTH_SHORT).show();
            } else {
                System.out.println("Website content:");
                System.out.println(document.text());

                Elements els = document.select("p");
                int i = 0;
                String data = "";
                for (Element ele : els) {
                    if (i > 5)
                        data = data + ele.text();
                    ++i;
                }

                TextView text = (TextView) findViewById(R.id.content_txt);
                text.setText(data);
            }

            mProgressDialog.dismiss();
        }
    }

}