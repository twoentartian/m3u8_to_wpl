import os
import xml.dom.minidom as minidom


def find_m3u_files(directory):
    m3u_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".m3u8"):
                m3u_files.append(os.path.join(root, file))
    return m3u_files


if __name__ == "__main__":
    current_directory = os.getcwd()
    m3u_files = find_m3u_files(current_directory)

    for m3u_file in m3u_files:
        songs = []
        with open(m3u_file, 'r') as file:
            songs = file.readlines()
            songs = songs[1:] # remove first line

        doc = minidom.Document()
        # Create the root element
        playlist = doc.createElement("smil")
        doc.appendChild(playlist)
        head = doc.createElement("head")
        playlist.appendChild(head)
        meta = doc.createElement("meta")
        meta.setAttribute("name", "Generator")
        meta.setAttribute("content", "Microsoft Windows Media Player -- 12.0.17134.472")
        head.appendChild(meta)
        body = doc.createElement("body")
        playlist.appendChild(body)
        seq = doc.createElement("seq")
        body.appendChild(seq)
        # Add media entries to the playlist
        media_entries = []
        for song in songs:
            song = song.replace("\n", "")
            filename = os.path.basename(song)
            print(filename)
            media_entries.append({"src": song, "title": filename})

        for entry in media_entries:
            media = doc.createElement("media")
            media.setAttribute("src", entry["src"])
            media.setAttribute("title", entry["title"])
            seq.appendChild(media)

        # Save the WPL file
        wpl_filename = f"{m3u_file}.wpl"
        with open(wpl_filename, "w", encoding="utf-8") as wpl_file:
            wpl_file.write(doc.toprettyxml(indent="  "))


