#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<time.h>

#define MAX_tweet 140

// それぞれのデータごとに分割する
void write_tweet(FILE *fp, char *tweet_buffer)
{
    if(strlen(tweet_buffer)>0)
    {
        fprintf(fp,"%s\n---\n",tweet_buffer);
    }
}

int main(void)
{
    // 今日の日付を取得
    time_t currentTime = time(NULL);
    struct tm *localTime = localtime(&currentTime);
    char today[20];

    sprintf(today,"%d/%d/%d",
           localTime->tm_year + 1900,
            localTime->tm_mon + 1,
            localTime->tm_mday);

            printf("today is %s\n",today);



    FILE *fp1,*fp2,*fp3,*fp4;
    char buffer[1024];
    char tweet_buffer[8192]="";

    // データを書き込むファイルを開く
    fp4=fopen("info_tweet.txt","w");
    if(fp4==NULL)
    {
        printf("can't open file info_tweet.txt\n");
        exit(1);
    }

    // 題名をまとめる
    fprintf(fp4,"🐸今日(%s)の蛙亭🐸\n",today);

    // 劇場情報をまとめる
    fp1=fopen("theater.csv","r");

    if(fp1==NULL)
    {
        printf("can't open file theater.csv\n");
        exit(1);
    }
    // ファイルから一行読み込む
    fgets(buffer,sizeof(buffer),fp1);

    // ファイルの終わりまで繰り返す
    while(fgets(buffer,sizeof(buffer),fp1))
    {
        char *token;
        int a=0;
        char *a1=NULL,*a2=NULL, *a5=NULL, *a6=NULL;

        token=strtok(buffer,",");

        // 区切られている文字列を順番に処理
        while(token!=NULL)
        {
            a++;
          
             if(a==1)
            {
                a1=token;
            }

              if(a==2)
            {
                a2=token;
            }

            if(a==5)
            {
                a5=token;
            }

            if(a==6)
            {
                a6=token;
            }

            // 次の文字列を取得する
            token=strtok(NULL,",");
        }
            
            // a2の中で今日の日付が含まれているものを抽出する
            if(a2&&strstr(a2,today))  
            {
              
                char today_data[512];
                sprintf(today_data,"【ライブ】\n%s\n@%s\n%s\n",a1,a5,a6);
            
                // 文字数が制限を超えたら一度書き出す
                if(strlen(tweet_buffer)+strlen(today_data)>MAX_tweet)
                {
                    write_tweet(fp4,tweet_buffer);
                    strcpy(tweet_buffer,"");
                }

                strcat(tweet_buffer,today_data);
            }
        
          
        
    }


    // メディア情報をまとめる
    fp2=fopen("kaeruTV.csv","r");
    if(fp2==NULL)
    {
        printf("can't open file kaeruTV.csv\n");
        exit(1);
    }

    fgets(buffer,sizeof(buffer),fp2);

    while(fgets(buffer,sizeof(buffer),fp2))
    {
       char *token;
       int b=0;
       char *b1=NULL, *b2=NULL, *b3=NULL, *b4=NULL, *b5=NULL, *b6=NULL;
       token=strtok(buffer,",");
       while(token!=NULL)
        {
            b++;
            if(b==1)
            {
                b1=token;
            }

            if(b==2)
            {
                b2=token;
            }

            if(b==3)
            {
                b3=token;
            }

            if(b==4)
            {
                b4=token;
            }

            if(b==5)
            {
                b5=token;
            }

            if(b==6)
            {
                b6=token;
            }

            token=strtok(NULL,",");
       }

    
            if(b2&&strstr(b2,today))
            {

                char today_data[512];
                sprintf(today_data,"【メディア】\n%s\n%s-%s\n@%s\n※%s\n",b1,b3,b4,b5,b6);
            

                if(strlen(tweet_buffer)+strlen(today_data)>MAX_tweet)
                {
                    write_tweet(fp4,tweet_buffer);
                    strcpy(tweet_buffer,"");
                }
                
                strcat(tweet_buffer,today_data);
            }
        
    }

    // レギュラー出演の情報
    if(localTime->tm_wday==3)
    {
        char reg[256]="【メディア】≪レギュラー≫\nこれ余談なんですけど…\n@ABCテレビ\n23:10-24:17\n※イワクラさんのみ、ナレーターで出演\n";
        if(strlen(tweet_buffer)+strlen(reg)>MAX_tweet)
        {
            write_tweet(fp4,tweet_buffer);
            strcpy(tweet_buffer,"");
        }
        strcat(tweet_buffer,reg);
    }
    if(localTime->tm_wday==0)
    {
        char reg[256]="【メディア】≪レギュラー≫\nポケモンとどこ行く!?\n@テレビ東京\n7:30-8:30\n※中野さんのみ、ナレーターで出演\n";
        if(strlen(tweet_buffer)+strlen(reg)>MAX_tweet)
        {
            write_tweet(fp4,tweet_buffer);
            strcpy(tweet_buffer,"");
        }
        strcat(tweet_buffer,reg);

    }
        
    

    // その他の情報をまとめる
    fp3=fopen("other.csv","r");
    if(fp3==NULL)
    {
        printf("can't open file other.csv\n");
        exit(1);
    }

    fgets(buffer,sizeof(buffer),fp3);
    while(fgets(buffer,sizeof(buffer),fp3))
    {
        char *token;
        int c=0;
        char *c1=NULL, *c2=NULL,*c3=NULL, *c5=NULL, *c6=NULL;
        token=strtok(buffer,",");
        while(token!=NULL)
        {
            c++;
            if(c==1)
            {
                c1=token;
            }

            if(c==2)
            {
                c2=token;
            }

            if(c==3)
            {
                c3=token;
            }

            if(c==5)
            {
                c5=token;
            }

            if(c==6)
            {
                c6=token;
            }

            token=strtok(NULL,",");

        }
        
            if(c2&&strstr(c2,today))
            {
                char today_data[512];
                sprintf(today_data,"【その他】\n%s\n@%s\n%s-\n※%s\n",c1,c5,c3,c6);
            

            if(strlen(tweet_buffer)+strlen(today_data)>MAX_tweet)
            {
                write_tweet(fp4,tweet_buffer);
                strcpy(tweet_buffer,"");
            }
            strcat(tweet_buffer,today_data);
            }

    
    }

    write_tweet(fp4,tweet_buffer);


    fclose(fp1);
    fclose(fp2);
    fclose(fp3);
    fclose(fp4);
  
}